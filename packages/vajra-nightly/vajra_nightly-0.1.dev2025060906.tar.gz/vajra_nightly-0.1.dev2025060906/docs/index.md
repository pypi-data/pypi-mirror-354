# Vajra Documentation


The landscape of artificial intelligence is undergoing a seismic shift. We are moving beyond AI that assists to AI that understands, reasons, and acts with increasing autonomy. This next generation — characterized by long-term memory, multimodal perception, and collaborative intelligence — demands a new class of infrastructure. Existing serving systems, designed for the chatbot era, no longer satisfy the growing needs of this shifting landscape **Vajra** is a low-latency distributed LLM inference serving engine built for serving these second-wave applications.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![CUDA 12.6+](https://img.shields.io/badge/CUDA-12.6+-green.svg)](https://developer.nvidia.com/cuda-downloads)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/project-vajra/vajra/blob/main/LICENSE)

## Key Features

🚀 **High Performance**  
Optimized C++ core with CUDA kernels for maximum throughput

⚡ **Low Latency**  
Advanced scheduling algorithms and memory management for minimal response times

🔧 **Flexible Scheduling**  
Multiple scheduling strategies to handle different types of workloads and latency constraints

📊 **Rich Monitoring**  
Built-in metrics collection and visualization for performance optimization

## Quick Start

```python
from vajra import InferenceEngine, SamplingParams
from vajra.config import InferenceEngineConfig, ModelConfig

# Configure the engine
model_config = ModelConfig(model="meta-llama/Llama-2-7b-hf")
engine_config = InferenceEngineConfig(model_config=model_config)

# Create engine and generate
engine = InferenceEngine(engine_config)
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)

engine.add_request("req1", "Tell me about quantum computing", sampling_params)

for output in engine.get_outputs():
    if output.finished:
        print(f"Generated: {output.outputs[0].text}")
```

## Documentation

```{toctree}
:maxdepth: 2
:caption: Getting Started

quickstart
troubleshooting
```

```{toctree}
:maxdepth: 2
:caption: Usage Guide

usage/index
```

```{toctree}
:maxdepth: 2
:caption: System Design

design/index
```

```{toctree}
:maxdepth: 2
:caption: Development

contributing/index
```

```{toctree}
:maxdepth: 2
:caption: Community

community/index
```

## Indices and Tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
