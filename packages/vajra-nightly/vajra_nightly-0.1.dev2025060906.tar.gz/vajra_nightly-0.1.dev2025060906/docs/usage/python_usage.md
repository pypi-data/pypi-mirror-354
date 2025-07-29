# Python Usage Guide

This page covers practical usage of Vajra's Python API with examples and common patterns. For complete auto-generated API documentation, see the [API Reference](api_reference/index.md).

## Quick Example

```python
from vajra import InferenceEngine, SamplingParams
from vajra.config import (
    InferenceEngineConfig, 
    LLMReplicaSetControllerConfig,
    LLMBaseReplicaControllerConfig,
    ModelConfig
)

# Configure the engine
model_config = ModelConfig(
    model="meta-llama/Llama-2-7b-chat-hf",
    dtype="float16"
)

replica_controller_config = LLMBaseReplicaControllerConfig(
    model_config=model_config
)

controller_config = LLMReplicaSetControllerConfig(
    replica_controller_config=replica_controller_config,
    num_replicas=1
)

engine_config = InferenceEngineConfig(
    controller_config=controller_config
)

# Create engine
engine = InferenceEngine(engine_config)

# Generate text
sampling_params = SamplingParams(
    temperature=0.7,
    max_tokens=100
)

engine.add_request(
    request_id="req_1",
    prompt="Explain quantum computing in simple terms:",
    sampling_params=sampling_params
)

# Get results
for output in engine.get_outputs():
    if output.finished:
        print(f"Generated: {output.outputs[0].text}")
        break
```

## Core Classes

### InferenceEngine

The main interface for programmatic inference.

```python
from vajra import InferenceEngine

engine = InferenceEngine(config)
```

**Methods:**

- `add_request(request_id: str, prompt: str, sampling_params: SamplingParams)` - Add a generation request
- `get_outputs() -> Iterator[RequestOutput]` - Get completed outputs
- `abort_request(request_id: str)` - Cancel a pending request
- `get_model_config() -> ModelConfig` - Get model configuration
- `get_num_unfinished_requests() -> int` - Number of pending requests

### SamplingParams

Controls text generation behavior:

```python
from vajra import SamplingParams

params = SamplingParams(
    temperature=0.7,        # Randomness (0.0 = deterministic)
    top_p=0.9,             # Nucleus sampling
    top_k=50,              # Top-k sampling  
    max_tokens=100,        # Max tokens to generate
    stop_strings=["\\n\\n"], # Stop sequences
    logprobs=None,         # Return log probabilities
    seed=None              # Random seed
)
```

**Key Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | float | 1.0 | Controls randomness (0.0-2.0) |
| `top_p` | float | 1.0 | Nucleus sampling threshold |
| `top_k` | int | -1 | Top-k sampling (-1 = disabled) |
| `max_tokens` | int | 16 | Maximum tokens to generate |
| `stop_strings` | List[str] | [] | Stop generation sequences |
| `frequency_penalty` | float | 0.0 | Frequency penalty (-2.0 to 2.0) |
| `presence_penalty` | float | 0.0 | Presence penalty (-2.0 to 2.0) |
| `logprobs` | int | None | Number of log probs to return |
| `seed` | int | None | Random seed for reproducibility |

### RequestOutput

Contains the results of a generation request:

```python
for output in engine.get_outputs():
    print(f"Request ID: {output.request_id}")
    print(f"Prompt: {output.prompt}")
    print(f"Finished: {output.finished}")
    
    if output.finished:
        completion = output.outputs[0]
        print(f"Generated text: {completion.text}")
        print(f"Token count: {len(completion.token_ids)}")
        print(f"Finish reason: {completion.finish_reason}")
```

**Attributes:**

- `request_id: str` - Unique request identifier
- `prompt: str` - Input prompt text
- `outputs: List[CompletionOutput]` - Generated completions
- `finished: bool` - Whether generation is complete

## Next Steps

- **[Configuration Reference](configuration.md)** - Complete configuration options and tuning
- **[OpenAI Server](openai_server.md)** - Production-ready server deployment
- **[API Reference](api_reference/index.md)** - Complete auto-generated API documentation