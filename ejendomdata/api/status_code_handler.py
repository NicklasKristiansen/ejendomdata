from __future__ import annotations
from .http_response_dispatch import response_dispatch
import logging, time, httpx
logger = logging.getLogger(__name__)
__all__ = ["status_code_handler"]

@response_dispatch
def status_code_handler(response: httpx.Response) -> httpx.Response:
    return response.raise_for_status()

@status_code_handler.register(429, 503, 408, 500, 502, 504)
def handle_downtime(response: httpx.Response, *, wait_time=0.5, max_tries=5):
    request = response.request
    tries = 1

    with httpx.Client() as client:
        while tries < max_tries and response.status_code not in (200, 202, 204):
            logger.warning(
                f"Received status code: {response.status_code} - waiting {wait_time:.1f}s "
                f"try {tries}/{max_tries} for {request.method} {request.url}"
            )
            time.sleep(wait_time)
            try:
                response = client.send(request)
            except httpx.HTTPError as e:
                logger.error(f"Retry failed with error: {e}")
                raise e
            tries += 1
            wait_time *= 2

    if response.status_code not in (200, 202, 204):
        raise httpx.HTTPStatusError(
            f"Received status code {response.status_code} after retrying {max_tries} times",
            request=request,
            response=response,
        )

    if response.status_code == 204:
        logger.warning(f"Empty response (204 No Content) from request to: {request.url}")

    return response
        

@status_code_handler.register(400)
def handle_bad_request(response: httpx.Response):
    logger.error(f"Bad Request (400): {response.text}")
    raise httpx.HTTPStatusError("Bad Request", request=response.request, response=response)


@status_code_handler.register(401)
def handle_unauthorized(response: httpx.Response):
    logger.error(f"Unauthorized (401) for request to {response.request.url}")
    raise httpx.HTTPStatusError("Unauthorized", request=response.request, response=response)


@status_code_handler.register(403)
def handle_forbidden(response: httpx.Response):
    logger.error(f"Forbidden (403): Access denied to {response.request.url}")
    raise httpx.HTTPStatusError("Forbidden", request=response.request, response=response)


@status_code_handler.register(404)
def handle_not_found(response: httpx.Response):
    logger.warning(f"Not Found (404): {response.request.url}")
    raise httpx.HTTPStatusError("Resource not found", request=response.request, response=response)


@status_code_handler.register(422)
def handle_unprocessable_entity(response: httpx.Response):
    logger.error(f"Unprocessable Entity (422): {response.text}")
    raise httpx.HTTPStatusError("Unprocessable Entity", request=response.request, response=response)
