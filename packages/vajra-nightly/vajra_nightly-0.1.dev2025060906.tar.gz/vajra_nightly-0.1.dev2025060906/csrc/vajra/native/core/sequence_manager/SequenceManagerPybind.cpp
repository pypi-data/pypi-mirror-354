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
#include "native/core/sequence_manager/SequenceManagerPybind.h"
//==============================================================================
#include "commons/TorchCommon.h"
#include "native/core/Types.h"
#include "native/core/sequence_manager/EngineSequenceManager.h"
#include "native/core/sequence_manager/WorkerSequenceManager.h"
//==============================================================================
namespace vajra {
//==============================================================================
// BaseSequenceManager has pure virtual methods. pybind fails to generate
// bindings without explicitly marking them pure. Define a wrapper that marks
// them pure. See:
// https://pybind11.readthedocs.io/en/stable/advanced/classes.html#overriding-virtual-functions-in-python
class PySequenceManager : BaseSequenceManager {
  using BaseSequenceManager::BaseSequenceManager;

  std::vector<int> GetBlockTable(SequencePtr) const override {
    PYBIND11_OVERRIDE_PURE(std::vector<int>, BaseSequenceManager,
                           GetBlockTable);
  }
};
//==============================================================================
void InitBaseSequenceManagerPybindClass(py::module& m) {
  py::class_<BaseSequenceManager, PySequenceManager,
             std::shared_ptr<BaseSequenceManager>>(m, "BaseSequenceManager")
      .def("add_sequence", &BaseSequenceManager::AddSequence)
      .def("get_seq", &BaseSequenceManager::GetSequence)
      .def("on_schedule", &BaseSequenceManager::OnSchedule)
      .def("on_step_completed", &BaseSequenceManager::OnStepCompleted)
      .def("on_stage_completed", &BaseSequenceManager::OnStageCompleted)
      .def("generate_request_outputs",
           &BaseSequenceManager::GenerateRequestOutputs);
}
//==============================================================================
void InitEngineSequenceManagerPybindClass(py::module& m) {
  py::class_<EngineSequenceManager, BaseSequenceManager,
             std::shared_ptr<EngineSequenceManager>>(m, "EngineSequenceManager")
      .def(py::init<std::shared_ptr<Tokenizer>, bool>(), py::arg("tokenizer"),
           py::arg("enable_sequence_pipeline_parallel"));
}
//==============================================================================
void InitWorkerSequenceManagerPybindClass(py::module& m) {
  py::class_<WorkerSequenceManager, BaseSequenceManager,
             std::shared_ptr<WorkerSequenceManager>>(m, "WorkerSequenceManager")
      .def(py::init<std::size_t, std::size_t, std::size_t, std::size_t, Rank,
                    KvpGroupId, std::size_t, bool>(),
           py::arg("block_size"), py::arg("num_gpu_blocks"),
           py::arg("max_model_len"), py::arg("max_num_tokens_per_kvp_group"),
           py::arg("rank"), py::arg("kvp_group_id"),
           py::arg("kvp_parallel_world_size"),
           py::arg("enable_sequence_pipeline_parallel"));
}
//==============================================================================
void InitOnScheduleResultPybindClass(py::module& m) {
  py::class_<OnScheduleResult>(m, "OnScheduleResult")
      .def(py::init<MutableSequences, MutableSequences,
                    std::optional<SequenceMetadataVector>>())
      .def_readonly("ignored_seqs", &OnScheduleResult::ignored_seqs)
      .def_readonly("scheduled_seqs", &OnScheduleResult::scheduled_seqs)
      .def_readonly("sequence_metadata_list",
                    &OnScheduleResult::sequence_metadata_list);
}
//==============================================================================
void InitSequenceManagerPybindSubmodule(py::module& pm) {
  auto m =
      pm.def_submodule("sequence_manager", "BaseSequenceManager submodule");

  InitOnScheduleResultPybindClass(m);
  InitBaseSequenceManagerPybindClass(m);
  InitEngineSequenceManagerPybindClass(m);
  InitWorkerSequenceManagerPybindClass(m);
}
//==============================================================================
}  // namespace vajra
//==============================================================================
