import json
import uuid
from http import HTTPStatus

import aiohttp
from aiohttp import web
from loguru import logger

from .chat import (
    prepare_request_data,
    send_non_streaming_request,
    send_streaming_request,
)
from .config import ArgoConfig
from .utils import make_bar

# Configuration variables


def make_it_openai_completions_compat(
    custom_response,
    model_name,
    create_timestamp,
    prompt_tokens,
    is_streaming=False,
    finish_reason=None,
):
    """
    Converts the custom API response to an OpenAI compatible API response.

    :param custom_response: JSON response from the custom API.
    :param model_name: The model used for the completion.
    :param create_timestamp: Timestamp for the completion.
    :param prompt_tokens: The input prompt token count used in the request.
    :return: OpenAI compatible JSON response.
    """
    try:
        # Parse the custom response
        if isinstance(custom_response, str):
            custom_response_dict = json.loads(custom_response)
        else:
            custom_response_dict = custom_response

        # Extract the response text
        response_text = custom_response_dict.get("response", "")

        # Calculate token counts (simplified example, actual tokenization may differ)
        if not is_streaming:
            completion_tokens = len(response_text.split())
            total_tokens = prompt_tokens + completion_tokens

        # Construct the OpenAI compatible response
        openai_response = {
            "id": f"cmpl-{uuid.uuid4().hex}",  # Unique ID
            "object": "text_completion",  # Object type
            "created": create_timestamp,  # Current timestamp
            "model": model_name,  # Model name
            "choices": [
                {
                    "text": response_text,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "stop",  # TODO: stop or length or ""/None
                }
            ],
        }
        if not is_streaming:
            openai_response["usage"] = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            }
        return openai_response

    except json.JSONDecodeError as err:
        return {"error": f"Error decoding JSON: {err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}


async def proxy_request(
    request: web.Request,
    *,
    convert_to_openai=False,
):
    """Proxies the request to the upstream API, handling both streaming and non-streaming modes.

    Args:
        convert_to_openai: Whether to convert the response to OpenAI-compatible format.
            Defaults to False.
        request: The web request object containing incoming request data.
        input_data: Optional input data (used for testing). If None, the request JSON
            data will be used.
        stream: Whether to enable streaming mode. Defaults to False.

    Returns:
        A web.Response object from the upstream API.

    Raises:
        ValueError: If the input data is invalid or missing.
        aiohttp.ClientError: If the HTTP request fails.
        Exception: For unexpected server or runtime errors.
    """
    config: ArgoConfig = request.app["config"]
    try:
        # Retrieve the incoming JSON data from request if input_data is not provided
        data = await request.json()
        stream = data.get("stream", False)

        if not data:
            raise ValueError("Invalid input. Expected JSON data.")
        if config.verbose:
            logger.info(make_bar("[completion] input"))
            logger.info(json.dumps(data, indent=4))
            logger.info(make_bar())

        # Prepare the request data
        data = prepare_request_data(data, request)

        # Determine the API URL based on whether streaming is enabled
        api_url = config.argo_stream_url if stream else config.argo_url

        # Forward the modified request to the actual API using aiohttp
        async with aiohttp.ClientSession() as session:
            if stream:
                return await send_streaming_request(
                    session,
                    api_url,
                    data,
                    request,
                    convert_to_openai,
                    openai_compat_fn=make_it_openai_completions_compat,
                )
            else:
                return await send_non_streaming_request(
                    session,
                    api_url,
                    data,
                    convert_to_openai,
                    openai_compat_fn=make_it_openai_completions_compat,
                )

    except ValueError as err:
        return web.json_response(
            {"error": str(err)},
            status=HTTPStatus.BAD_REQUEST,
            content_type="application/json",
        )
    except aiohttp.ClientError as err:
        error_message = f"HTTP error occurred: {err}"
        return web.json_response(
            {"error": error_message},
            status=HTTPStatus.SERVICE_UNAVAILABLE,
            content_type="application/json",
        )
    except Exception as err:
        error_message = f"An unexpected error occurred: {err}"
        return web.json_response(
            {"error": error_message},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            content_type="application/json",
        )
