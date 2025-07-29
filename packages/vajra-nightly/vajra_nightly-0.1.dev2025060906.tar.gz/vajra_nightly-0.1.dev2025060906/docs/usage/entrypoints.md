# Entrypoints and Deployment Options

Vajra provides multiple entrypoints designed for different use cases, from production serving to development and performance evaluation. This guide helps you choose the right entrypoint for your needs.

## Available Entrypoints

### OpenAI-Compatible API Server (Production)

**Primary entrypoint for production deployments**

Command: `python -m vajra.entrypoints.openai.api_server`

#### Key Features
- **OpenAI Compatibility**: Drop-in replacement for OpenAI API with support for `/v1/chat/completions` and `/v1/completions`
- **Streaming Support**: Real-time response streaming
- **Authentication**: API key-based security

For detailed API server documentation refer to [OpenAI Server Usage Guide](openai_server.md).

### Benchmark Runner (Performance Evaluation)

**For measuring performance and load testing**

Command: `python -m vajra.benchmark.main`

#### Key Features
- **Workload Generation**: Multiple request patterns (synthetic, trace-based)
- **Request Patterns**: Configurable arrival patterns (Poisson, Gamma, static)
- **Length Distributions**: Various request length generators
- **Metrics Collection**: Detailed performance metrics
- **Experiment Tracking**: WandB integration

For detailed benchmark runner documentation, see [Benchmark Runner Guide](benchmark_runner.md).

### Offline Inference (Development & Batch Processing)

**For development, debugging, and batch processing**

Implementation: Direct Python API using `InferenceEngine` class

#### Key Features
- **Configuration Flexibility**: Full access to all engine options
- **Development Friendly**: Easy debugging and introspection

See [Python Usage Guide](python_usage.md) for implementation details.

## Next Steps

- For production deployment: See [OpenAI Server Guide](openai_server.md)
- For performance evaluation: See [Benchmark Runner Guide](benchmark_runner.md)
- For configuration details: See [Configuration Reference](configuration.md)  
- For API usage: See [Python Usage Guide](python_usage.md) 