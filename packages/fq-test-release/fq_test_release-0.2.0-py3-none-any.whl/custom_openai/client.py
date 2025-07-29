from openai import OpenAI, AsyncOpenAI
import logging
from typing import Any, Callable, Coroutine, Union

logger = logging.getLogger("CustomOpenAIClient")

def format_response(response) -> dict:
    if not response or not hasattr(response, 'choices') or not response.choices:
        raise ValueError("Invalid OpenAI response: 'choices' field is missing.")
    choice = response.choices[0]
    message_content = getattr(choice.message, "content", None)
    if not message_content:
        raise ValueError("Message content is missing in the response.")
    return {
        "success": True,
        "content": message_content.strip(),
        "model": getattr(response, "model", "unknown"),
        "usage": {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
            "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0)
        },
        "finish_reason": getattr(choice, "finish_reason", "unknown")
    }

def handle_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"[Unhandled Error] {type(e).__name__}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
    return wrapper

def handle_async_errors(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"[Unhandled Error] {type(e).__name__}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
    return wrapper

class CustomOpenAIClient(OpenAI):
    """
    Custom OpenAI client with robust error handling and standardized responses.
    """

    @handle_errors
    def chat_completions_create(self, *args, **kwargs) -> dict:
        response = self.chat.completions.create(*args, **kwargs)
        return format_response(response)

class CustomAsyncOpenAIClient(AsyncOpenAI):
    """
    Custom asynchronous OpenAI client with robust error handling and standardized responses.
    """

    @handle_async_errors
    async def chat_completions_create(self, *args, **kwargs) -> dict:
        response = await self.chat.completions.create(*args, **kwargs)
        return format_response(response)
