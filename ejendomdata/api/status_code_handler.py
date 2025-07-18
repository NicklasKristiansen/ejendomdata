from __future__ import annotations
from .http_response_dispatch import response_dispatch
import logging
import time
import httpx
logger = logging.getLogger(__name__)


@response_dispatch()
def status_code_handler(response: httpx.Response):
    return response.raise_for_status()

@status_code_handler.register(429, 503)
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
                raise e  # re-raise original error
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
        

# TODO: handle other cases

    


