# OpenAI-Compatible Server

The most common way to use Vajra is through its OpenAI-compatible API server. This allows you to use Vajra as a drop-in replacement for OpenAI's API while benefiting from Vajra's high-performance inference capabilities.

## Launching Server

```bash
# Start server with default settings (Llama-3-8B-Instruct)
python -m vajra.entrypoints.openai.api_server

# Start with a specific model
python -m vajra.entrypoints.openai.api_server \
    --model_config_model meta-llama/Llama-2-7b-chat-hf
```

The server will start on `http://localhost:8000` by default.

> **For detailed configuration options**: See the [Configuration Reference](configuration.md) which covers all scheduling strategies, parallelism options, and performance tuning parameters.

## Sending Requests

Once the server is running, you can use it with any OpenAI-compatible client:

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy"  # API key can be anything if not configured
)

response = client.chat.completions.create(
    model="meta-llama/Llama-2-7b-chat-hf",  # Must match the loaded model
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    max_tokens=100,
    temperature=0.7
)

print(response.choices[0].message.content)
```

you could also do this using curl:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy" \
  -d '{
    "model": "meta-llama/Llama-2-7b-chat-hf",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

## API Compatibility

Vajra's OpenAI server supports the following endpoints:

- **Chat Completions**: `/v1/chat/completions`
- **Completions**: `/v1/completions` 
- **Models**: `/v1/models`

### Supported Parameters

**Chat Completions:**
- `model` - Model identifier (must match loaded model)
- `messages` - Array of message objects
- `max_tokens` - Maximum tokens to generate
- `temperature` - Sampling temperature (0.0 to 2.0)
- `top_p` - Nucleus sampling parameter
- `top_k` - Top-k sampling parameter
- `frequency_penalty` - Frequency penalty
- `presence_penalty` - Presence penalty
- `stop` - Stop sequences
- `stream` - Stream responses

## Next Steps

- **[Configuration Reference](configuration.md)** - Complete configuration options and performance tuning
- **[Python Usage Guide](python_usage.md)** - Advanced programmatic usage
- **[API Reference](api_reference/index.md)** - Complete auto-generated API documentation 