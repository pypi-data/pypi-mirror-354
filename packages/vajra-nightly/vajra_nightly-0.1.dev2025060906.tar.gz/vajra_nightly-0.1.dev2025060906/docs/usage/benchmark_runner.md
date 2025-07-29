# Benchmark Runner Guide

The Vajra benchmark runner is a comprehensive tool for performance evaluation, load testing, and system characterization. It enables systematic measurement of inference throughput, latency, and resource utilization under various workload conditions.

## Overview

The benchmark runner (`python -m vajra.benchmark.main`) generates synthetic or trace-based workloads to evaluate system performance across different configurations, models, and deployment scenarios.

### Key Capabilities

- **Workload Generation**: Synthetic and trace-based request patterns
- **Performance Metrics**: Throughput, latency, resource utilization
- **Load Testing**: Stress testing with configurable request rates
- **Experiment Tracking**: Integration with Weights & Biases (WandB)
- **Comparative Analysis**: Multi-configuration benchmarking

## Workload Types

### Synthetic Workloads

**Poisson Arrival Pattern**
- Simulates realistic user request patterns
- Configurable average request rate
- Natural variation in request timing

**Gamma Distribution**
- More controlled request spacing
- Suitable for stress testing specific scenarios
- Configurable shape and scale parameters

**Static Rate**
- Fixed interval between requests
- Deterministic load patterns
- Useful for baseline measurements

### Trace-Based Workloads

**Real Traffic Replay**
- Uses actual production request traces
- Preserves original timing and length patterns
- Enables realistic performance evaluation

**Custom Trace Format**
- JSON format with request metadata
- Configurable prompt lengths and timing
- Supports batch processing scenarios

## Request Length Generation

### Distribution Types

**Uniform Distribution**
- Fixed or range-based prompt lengths
- Simple baseline measurements
- Consistent resource utilization

**Normal Distribution**
- Realistic length variation
- Configurable mean and standard deviation
- Models typical user behavior

**Exponential Distribution**
- Heavy-tailed length distribution
- Tests performance under variable load
- Simulates diverse use cases

**Trace-Based Lengths**
- Extracted from real usage data
- Preserves actual length patterns
- Most realistic evaluation

