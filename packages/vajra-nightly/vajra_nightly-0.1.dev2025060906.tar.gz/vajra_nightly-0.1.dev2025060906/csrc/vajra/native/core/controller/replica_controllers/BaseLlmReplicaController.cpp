//==============================================================================
// Copyright 2025 Vajra Team; Georgia Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//==============================================================================
#include "native/core/controller/replica_controllers/BaseLlmReplicaController.h"
//==============================================================================
#include "commons/Time.h"
#include "native/core/Types.h"
#include "native/utils/ZmqHelper.h"
//==============================================================================
namespace vajra {
//==============================================================================
BaseLlmReplicaController::BaseLlmReplicaController(
    ReplicaId replica_id, std::shared_ptr<LlmReplicaControllerConfig> config,
    std::shared_ptr<BaseRequestPrioritizer> request_prioritizer,
    CommInfoPtr comm_info, SequencePriorityQueuePtr waiting_seq_queue,
    RequestOutputQueuePtr output_queue,
    std::shared_ptr<BaseReplicaScheduler> scheduler,
    std::shared_ptr<EngineSequenceManager> sequence_manager,
    std::shared_ptr<EngineMetricsStore> metrics_store)
    : BaseReplicaController(replica_id, config, request_prioritizer,
                            waiting_seq_queue, output_queue),
      scheduler_(scheduler),
      comm_info_(comm_info),
      sequence_manager_(sequence_manager),
      metrics_store_(metrics_store),
      replica_id_(replica_id) {
  ASSERT_VALID_POINTER_ARGUMENT(config);
  ASSERT_VALID_POINTER_ARGUMENT(request_prioritizer);
  ASSERT_VALID_POINTER_ARGUMENT(comm_info);
  ASSERT_VALID_POINTER_ARGUMENT(waiting_seq_queue);
  ASSERT_VALID_POINTER_ARGUMENT(output_queue);
  ASSERT_VALID_POINTER_ARGUMENT(scheduler);
  ASSERT_VALID_POINTER_ARGUMENT(sequence_manager);
  ASSERT_VALID_POINTER_ARGUMENT(metrics_store);

  InitZmqSockets();
  InitializeThreads();
}
//==============================================================================
void BaseLlmReplicaController::InitializeThreads() {
  controller_running_ = true;
  stop_worker_ = false;

  // Start the worker thread for async processing
  worker_thread_ =
      std::thread(&BaseLlmReplicaController::OutputProcessingLoop, this);

  // Start the scheduler thread
  scheduler_thread_ =
      std::thread(&BaseLlmReplicaController::SchedulerLoop, this);
}
//==============================================================================
void BaseLlmReplicaController::StopThreads() {
  controller_running_ = false;

  // Stop the worker thread
  stop_worker_ = true;
  // Push empty data to wake up worker thread
  output_data_queue_.push(RequestOutputData{});

  if (worker_thread_.joinable()) {
    worker_thread_.join();
  }

  if (scheduler_thread_.joinable()) {
    scheduler_thread_.join();
  }
}
//==============================================================================
BaseLlmReplicaController::~BaseLlmReplicaController() {
  StopThreads();
  CloseZmqSockets();
}
//==============================================================================
void BaseLlmReplicaController::BindZmqSocket(zmq::socket_t& socket,
                                             std::size_t port) {
  std::string endpoint = std::format("tcp://*:{}", port);

  for (std::size_t num_retries = 0;
       num_retries < kReplicaControllerZmqBindRetries; ++num_retries) {
    try {
      socket.bind(endpoint);
      return;
    } catch (const zmq::error_t& e) {
      LOG_WARNING("Failed to bind socket to {}: {}", endpoint, e.what());
      LOG_WARNING("Retrying in {} seconds...",
                  kReplicaControllerZmqBindBackoffS);
      std::this_thread::sleep_for(
          std::chrono::seconds(kReplicaControllerZmqBindBackoffS));
    }
  }

  THROW_RUNTIME_ERROR("Failed to bind socket to {} after {} retries", endpoint,
                      kReplicaControllerZmqBindRetries);
}
//==============================================================================
void BaseLlmReplicaController::InitZmqSockets() {
  zmq_context_ = zmq::context_t();
  enqueue_socket_ = zmq::socket_t(zmq_context_, zmq::socket_type::pub);
  output_socket_ = zmq::socket_t(zmq_context_, zmq::socket_type::pull);

  LOG_INFO("Initializing ZMQ sockets for replica controller {}", replica_id_);
  LOG_INFO("Initializing enqueue socket, binding to port {}",
           comm_info_->enqueue_socket_port);
  BindZmqSocket(enqueue_socket_, comm_info_->enqueue_socket_port);
  LOG_INFO("Initializing output socket, binding to port {}",
           comm_info_->output_socket_port);
  BindZmqSocket(output_socket_, comm_info_->output_socket_port);
}
//==============================================================================
void BaseLlmReplicaController::CloseZmqSockets() {
  enqueue_socket_.close();
  output_socket_.close();
  zmq_context_.close();
}
//==============================================================================
void BaseLlmReplicaController::OnStepCompleted(
    const SchedulerOutputPtr& scheduler_output, const MutableSequences& seqs,
    const ValidSamplerOutputs& sampler_outputs, const TimeS start_time) {
  // Process sequence manager updates
  sequence_manager_->OnStepCompleted(
      scheduler_output->seq_schedule_metadata_list, sampler_outputs);

  scheduler_->OnStepCompleted(
      seqs, static_cast<float>(time_utils::now_s() - start_time));
  // Update metrics
  metrics_store_->OnBatchEnd(AsConstSequences(seqs), scheduler_output,
                             start_time, time_utils::now_s());
}
//==============================================================================
void BaseLlmReplicaController::ProcessRequestOutputData(
    const RequestOutputData& data) {
  try {
    // The second parameter is not used in the engine append token
    for (auto seq : data.scheduled_seqs) {
      sequence_manager_->OnGenerateRequestOutput(seq);
    }

    std::vector<RequestOutputPtr> request_outputs =
        sequence_manager_->GenerateRequestOutputs(
            AsConstSequences(data.ignored_seqs),
            AsConstSequences(data.scheduled_seqs));

    // Push each request output to the output queue
    for (const auto& request_output : request_outputs) {
      output_queue_->push(request_output);
    }
  } catch (const std::exception& e) {
    LOG_ERROR("Exception processing request outputs for replica {}: {}",
              replica_id_, e.what());
  }
}
//==============================================================================
void BaseLlmReplicaController::OutputProcessingLoop() {
  LOG_INFO("Request output processing thread started for replica {}",
           replica_id_);

  while (!stop_worker_.load()) {
    RequestOutputData data;
    output_data_queue_.wait_pull(data);

    if (stop_worker_.load()) {
      break;
    }

    ProcessRequestOutputData(data);
  }

  LOG_INFO("Request output processing thread stopped for replica {}",
           replica_id_);
}
//==============================================================================
ValidSamplerOutputs BaseLlmReplicaController::CombineSamplerOutputs(
    const std::vector<SamplerOutputPtr>& all_workers_sampler_outputs,
    const SequenceScheduleMetadataPtrList& seq_schedule_metadata_list) {
  std::unordered_map<SeqId, SamplerOutputPtr> sampler_outputs_map;
  sampler_outputs_map.reserve(all_workers_sampler_outputs.size());

  for (const auto& output : all_workers_sampler_outputs) {
    if (output) {
      sampler_outputs_map[output->GetSeqId()] = output;
    }
  }

  ValidSamplerOutputs result;
  result.reserve(sampler_outputs_map.size());

  // Sort sampler outputs based on sequence schedule metadata
  for (const auto& metadata : seq_schedule_metadata_list) {
    if (sampler_outputs_map.find(metadata->seq_id) !=
        sampler_outputs_map.end()) {
      result.push_back(sampler_outputs_map[metadata->seq_id]);
    } else {
      ASSERT_VALID_RUNTIME(false, "sampler output not found for sequence {}",
                           metadata->seq_id);
    }
  }

  return result;
}
//==============================================================================
void BaseLlmReplicaController::Step() {
  auto start_time = time_utils::now_s();

  auto schedule_result = scheduler_->Schedule();

  if (schedule_result.scheduler_output->is_empty) {
    return;
  }

  for (const auto& seq : schedule_result.new_seqs) {
    sequence_manager_->AddSequence(seq);
  }

  auto on_schedule_result =
      sequence_manager_->OnSchedule(schedule_result.scheduler_output);

  auto end_time = time_utils::now_s();

  std::vector<SequenceParams> new_seq_params;
  for (const auto& seq : schedule_result.new_seqs) {
    new_seq_params.emplace_back(seq->GetParams());
  }

  auto step_inputs =
      StepInputs(schedule_result.scheduler_output, new_seq_params);

  ZmqHelper::Send<StepInputs>(enqueue_socket_, step_inputs);

  metrics_store_->OnSchedule(replica_id_, schedule_result.scheduler_output,
                             start_time, end_time);
  std::vector<SamplerOutputPtr> all_workers_sampler_outputs;

  std::size_t kv_parallel_size = GetConfig()->parallel_config.kv_parallel_size;

  for (std::size_t i = 0; i < kv_parallel_size; ++i) {
    StepOutputs step_outputs = ZmqHelper::Recv<StepOutputs>(output_socket_);
    ASSERT_VALID_RUNTIME(
        step_outputs.schedule_id == schedule_result.scheduler_output->id,
        "Schedule ID Mismatch");

    for (const auto& sampler_output : step_outputs.sampler_outputs) {
      if (sampler_output) {
        all_workers_sampler_outputs.push_back(sampler_output.value());
      }
    }
  }

  ValidSamplerOutputs sampler_outputs = CombineSamplerOutputs(
      all_workers_sampler_outputs,
      schedule_result.scheduler_output->seq_schedule_metadata_list);

  OnStepCompleted(schedule_result.scheduler_output,
                  on_schedule_result.scheduled_seqs, sampler_outputs,
                  start_time);

  // async request output processing - directly push data into queue
  output_data_queue_.push(RequestOutputData{
      schedule_result.scheduler_output->seq_schedule_metadata_list,
      on_schedule_result.ignored_seqs, on_schedule_result.scheduled_seqs});
}
//==============================================================================
void BaseLlmReplicaController::SchedulerLoop() {
  while (controller_running_) {
    Step();
  }
}
//==============================================================================
}  // namespace vajra
//==============================================================================
