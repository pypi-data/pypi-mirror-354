from openai import OpenAI, AsyncOpenAI
import logging
from typing import Any, Callable, Coroutine, Union

logger = logging.getLogger("CustomOpenAIClient")


def format_response(response, type) -> dict:

    # if type == "responses":
    #     model = getattr(response, "model", "unknown")
    #     if (
    #         not response
    #         or not hasattr(response, "output_text")
    #         or not response.output_text
    #     ):
    #         raise ValueError("Invalid OpenAI response: 'choices' field is missing.")
    #     message_content = response.output_text
    #     finish_reason = "stop"
    #     if not message_content:
    #         raise ValueError("Message content is missing in the response.")
    # else:
    #     model = getattr(response, "model", "unknown")
    #     if not response or not hasattr(response, "choices") or not response.choices:
    #         raise ValueError("Invalid OpenAI response: 'choices' field is missing.")
    #     choice = response.choices[0]
    #     message_content = getattr(choice.message, "content", None)
    #     finish_reason = getattr(choice, "finish_reason", None)

    #     if not message_content:
    #         raise ValueError("Message content is missing in the response.")

    return {
        # "success": True,
        # "content": message_content.strip(),
        # "model": model,
        # "usage": {
        #     "prompt_tokens": getattr(response.usage, "prompt_tokens", 0)
        #     or getattr(response.usage, "input_tokens", 0),
        #     "completion_tokens": getattr(response.usage, "completion_tokens", 0)
        #     or getattr(response.usage, "output_tokens", 0),
        #     "total_tokens": getattr(response.usage, "total_tokens", 0),
        # },
        # "finish_reason": finish_reason,
    }


class CustomOpenAIClient(OpenAI):
    """
    Custom OpenAI client with robust error handling and standardized responses.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Guarda referência ao método original
        original_responses_create = self.responses.create
        original_completions_create = self.chat.completions.create

        def custom_responses_create(*args, **kwargs):
            response = original_responses_create(*args, **kwargs)
            # response.flashquery = format_response(response, "responses")
            return response

        def custom_completions_create(*args, **kwargs):
            response = original_completions_create(*args, **kwargs)
            # response.flashquery = format_response(response, "completions")
            return response

        self.responses.create = custom_responses_create
        self.chat.completions.create = custom_completions_create


class CustomAsyncOpenAIClient(AsyncOpenAI):
    """
    Custom asynchronous OpenAI client with robust error handling and standardized responses.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        original_responses_create = self.responses.create
        original_completions_create = self.chat.completions.create

        self.full_text = ""

        def get_flash_query_stream(response, type: str) -> dict:
            return {
                # "success": True,
                # "content": (
                #     self.full_text.strip()
                #     if type == "completions"
                #     else response.response.output_text
                # ),
                # "model": (
                #     response.model
                #     if getattr(response, "model", "unknown")
                #     else response.response.model
                # ),
                # "usage": {
                #     "prompt_tokens": 0,
                #     "completion_tokens": 0,
                #     "total_tokens": 0,
                # },
                # "finish_reason": (
                #     response.choices[0].finish_reason if type == "completions" else "stop"
                # ),
            }

        # Wrap the async generator
        async def stream_wrapper(stream, type: str):
            """
            Async generator wrapper that yields all elements from the input stream,
            and injects a custom 'flashquery' field into the last item before yielding it.

            Args:
                stream: The original async generator.
                type: The type of the stream, used for generation (default is 'completions').
            """
            iterator = stream.__aiter__()
            try:
                previous = await iterator.__anext__()
            except StopAsyncIteration:
                return  # Stream is empty

            while True:
                try:
                    current = await iterator.__anext__()
                    if type == "completions":
                        self.full_text += previous.choices[0].delta.content
                    yield previous
                    previous = current
                except StopAsyncIteration:
                    # Last item reached, attach custom field and yield
                    try:
                        setattr(
                            previous,
                            "flashquery",
                            get_flash_query_stream(previous, type),
                        )
                    except Exception:
                        # Defensive: if previous does not support attributes
                        pass
                    yield previous
                    break
                except Exception as ex:
                    # Optional: handle/log unexpected generator errors
                    print(f"Stream error: {ex}")
                    raise

        async def custom_responses_create(*args, **kwargs):
            stream = kwargs.get("stream", False)
            response = await original_responses_create(*args, **kwargs)
            if stream:
                return stream_wrapper(response, "responses")
            else:
                # response.flashquery = format_response(response, "responses")
                return response

        async def custom_completions_create(*args, **kwargs):
            stream = kwargs.get("stream", False)
            response = await original_completions_create(*args, **kwargs)
            if stream:
                return stream_wrapper(response, "completions")
            else:
                # response.flashquery = format_response(response, "completions")
                return response

        self.responses.create = custom_responses_create
        self.chat.completions.create = custom_completions_create
