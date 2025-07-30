# custom-openai

A robust, user-friendly wrapper for the OpenAI Python package, featuring simplified response formatting and explicit error handling.

## Features

* **Clean and consistent responses**: Always get predictable output from your completions.
* **Automatic error handling**: Exceptions are caught and returned in a structured way.
* **Async and sync support**: Use the API in both synchronous and asynchronous Python projects.

## Installation

```bash
pip install custom-openai
```

## Usage

### Synchronous

```python
from custom_openai import CustomOpenAIClient

client = CustomOpenAIClient(api_key="your-api-key")
response = client.chat_completions_create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)
if response["success"]:
    print(response["content"])
else:
    print("Error:", response["error_type"], response["error_message"])
```

### Asynchronous

```python
import asyncio
from custom_openai import CustomAsyncOpenAIClient

async def main():
    client = CustomAsyncOpenAIClient(api_key="your-api-key")
    response = await client.chat_completions_create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=100
    )
    if response["success"]:
        print(response["content"])
    else:
        print("Error:", response["error_type"], response["error_message"])

asyncio.run(main())
```

## Response Format

All responses follow the same structure:

```python
{
    "success": True, # or False if there was an error
    "text": "...", # model output (only if success)
    "model": "...", # model used
    "usage": {
        "prompt_tokens": ...,
        "completion_tokens": ...,
        "total_tokens": ...
    },
    "finish_reason": "...", # reason for completion
    # Error fields (only present if success is False):
    "error_type": "...",
    "error_message": "..."
}
```

## License

MIT License
