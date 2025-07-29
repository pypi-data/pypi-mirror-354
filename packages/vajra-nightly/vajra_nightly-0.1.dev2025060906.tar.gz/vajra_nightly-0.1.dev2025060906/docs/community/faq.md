# Frequently Asked Questions

This page addresses common questions about Vajra.

## General Questions

### What is Vajra?

Vajra is a high-performance inference engine designed for large language models. It features hierarchical scheduling, memory-efficient execution, and sophisticated parallelism strategies to deliver low-latency, high-throughput text generation.

### How does Vajra compare to other inference engines?

Vajra differentiates itself through:

- **Hierarchical Scheduling**: Advanced scheduling algorithms that optimize for both throughput and latency
- **Parallelism Strategies**: Multiple parallelism techniques (tensor, pipeline, sequence) for different deployment scenarios, efficiently scaling to hundreds of GPUs
- **C++/Python Integration**: Core components implemented in C++ with Python bindings for performance
- **Event-Driven Architecture**: Asynchronous processing for improved resource utilization

### What models does Vajra support?

Vajra supports a wide range of transformer-based language models, including:

- LLaMA 3.1 (8B, 70B)
- Mistral (7B)
- Mixtral (8x7B)


## Usage Questions

### Can Vajra run on multiple machines?

Yes, Vajra supports distributed deployment across multiple machines. Just initialize resources Ray cluster across different all the machines, and Vajra would be able to automatically deploy across the entire cluster.

### Why is `CUDA_VISIBLE_DEVICES` not working?

Vajra has been designed to work with multiple machines in a distributed manner, which renders the `CUDA_VISIBLE_DEVICES` meaningless. There are three different approaches that can be used to limit the GPUs visible to Vajra:

1. Set `CUDA_VISIBLE_DEVICES` and manually launch the ray cluster.
2. Start docker container with `--gpus` flag.
3. Explicitly define `global_resource_mapping` in `InferenceEngineConfig`.


## Where can I get more help?

If you encounter issues not covered in this FAQ:

- Check the [Troubleshooting Guide](../troubleshooting.md) for common problems and solutions
- Report bugs on the [GitHub Issues page](https://github.com/project-vajra/vajra/issues)
- Join the community discussion on [Discord](https://discord.gg/wjaSvGgsNN)
- Refer to the [API Reference](../usage/api_reference/index.md) for detailed documentation
