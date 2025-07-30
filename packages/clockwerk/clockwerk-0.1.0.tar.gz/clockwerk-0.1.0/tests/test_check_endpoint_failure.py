import pytest
import aiohttp
from unittest.mock import patch
from aiohttp import ClientTimeout

from src.clockwerk.monitor import check_endpoint
from src.clockwerk.models import Endpoint
from src.clockwerk.config import EmailConfig

@pytest.mark.asyncio
async def test_check_endpoint_failure():
    endpoint = Endpoint(url="https://example.com", timeout=1)
    email = EmailConfig(
        smtp_host="smtp.mailtrap.io",
        smtp_port=587,
        email_from="test@example.com",
        email_to="admin@example.com"
    )

    with patch.object(aiohttp.ClientSession, "get", side_effect=ClientTimeout):
        async with aiohttp.ClientSession() as session:
            result = await check_endpoint(session, endpoint, email)

    assert not result.success
    assert result.status_code == 0
    assert "ClientTimeout" in result.error