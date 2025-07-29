# Troubleshooting

## Common Issues

### Installation Problems

**CUDA Version Mismatch**
```bash
# Check CUDA version
nvidia-smi
nvcc --version

# Reinstall with correct CUDA version
pip install -r requirements.txt --extra-index-url https://flashinfer.ai/whl/cu124/torch2.4/
```

## Debugging Tips

### Debug Build

For debugging C++ code issues, build with debug symbols enabled:

```bash
# Build with debug symbols (includes debugging information)
make build/native BUILD_TYPE=Debug

# For incremental builds during development
make build/native_incremental
```

**Debug vs Release builds:**
- `Debug` (default): Includes debug symbols, no optimization, easier debugging
- `Release`: Optimized for performance, smaller binaries, harder to debug

### Enable Debug Logs

Control logging verbosity using the `VAJRA_LOG_LEVEL` environment variable:

```bash
# Enable debug logging (most verbose)
export VAJRA_LOG_LEVEL=DEBUG
python your_script.py

# Other log levels
export VAJRA_LOG_LEVEL=INFO     # Default level
export VAJRA_LOG_LEVEL=WARNING  # Warnings and errors only
export VAJRA_LOG_LEVEL=ERROR    # Errors only
```

### Environment Diagnostics

**Collect environment information:**
```bash
# Print comprehensive environment info
python -m vajra.utils.collect_env
```

### Memory Issues

**Reduce build memory usage:**

```bash
# Limit parallel build jobs
export CMAKE_BUILD_PARALLEL_LEVEL=4

make build/native
```
