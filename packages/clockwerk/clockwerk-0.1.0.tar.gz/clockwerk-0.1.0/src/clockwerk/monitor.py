#-------------------- Imports --------------------

import asyncio
import aiohttp
import logging

from aiohttp import ClientError, ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from time import perf_counter

from src.clockwerk.models import MonitorResult, Endpoint
from src.clockwerk.config import EmailConfig
from src.clockwerk.logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Monitor Function --------------------

@retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ClientError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def _safe_session(session: aiohttp.ClientSession, url: str, timeout: int):
    async with session.get(url, timeout=ClientTimeout(total=timeout)) as resp:
        await resp.read()
        return resp


async def check_endpoint(
        session: aiohttp.ClientSession,
        endpoint: Endpoint,
        email_config: EmailConfig
    ) -> MonitorResult:
    """
    Summary:
    Sends an asynchronous request to a specified endpoint and records the ensuing result

    Description:
    - Initiates an aiohttp Client Session and makes initial request
    - Handles the response appropirately based on status code / latency
    - Produces a MonitorResult-object with relevant endpoint information

    Args:
        session (aiohttp.ClientSession): The HTTP Session used to perform the request
        endpoint (Endpoint): The target endpoint, including URL, timeout and alert settings
        email_config (EmailConfig): Configuration model containing SMTP Host, SMTP Port, recieving E-mail and sending E-mail

    Returns:
        MonitorResult: Model containing relevant information regarding the last endpoint check

    Raises:
        Exception: Raised if the request fails in a way not handled by Retry logic
    """
    url = str(endpoint.url)
    timeout = endpoint.timeout
    start = perf_counter()

    try:
        resp = await _safe_session(session, url, timeout)
        latency = perf_counter() - start
        logger.info(f"Endpoint check passed: {url} with {latency:.2f}s latency")

        return MonitorResult(
            endpoint_name=url,
            status_code=resp.status,
            latency=latency,
            success=resp.status == 200,
            error=None if resp.status == 200 else f"Unexpected status {resp.status}"
        )
    except Exception as err:
        latency = perf_counter() - start
        logger.exception("Unexpected exception occured")
        return MonitorResult(
            endpoint_name=url,
            status_code=0,
            latency=latency,
            success=False,
            error=str(err)
        )
