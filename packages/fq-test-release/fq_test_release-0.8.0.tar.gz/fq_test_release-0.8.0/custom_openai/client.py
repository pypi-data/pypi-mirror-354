from openai import OpenAI, AsyncOpenAI
import logging
from typing import Any, Callable, Coroutine, Union

logger = logging.getLogger("CustomOpenAIClient")


def format_response(response) -> dict:
    return getattr(response, "flashquery", {})


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
            response.flashquery = format_response(response)
            return response

        def custom_completions_create(*args, **kwargs):
            response = original_completions_create(*args, **kwargs)
            response.flashquery = format_response(response)
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
                            format_response(previous),
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
                response.flashquery = format_response(response)
                return response

        async def custom_completions_create(*args, **kwargs):
            stream = kwargs.get("stream", False)
            response = await original_completions_create(*args, **kwargs)
            if stream:
                return stream_wrapper(response, "completions")
            else:
                response.flashquery = format_response(response)
                return response

        self.responses.create = custom_responses_create
        self.chat.completions.create = custom_completions_create
