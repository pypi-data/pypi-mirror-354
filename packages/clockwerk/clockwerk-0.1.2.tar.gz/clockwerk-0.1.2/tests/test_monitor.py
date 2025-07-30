import pytest_asyncio
import pytest
from aiohttp import ClientSession
from src.clockwerk.models import Endpoint
from src.clockwerk.monitor import check_endpoint
from src.clockwerk.config import EmailConfig

@pytest.mark.asyncio
async def test_check_endpoint_success():
    endpoint = Endpoint(
        url="https://httpbin.org/status/200",
        timeout=20, 
        alert_threshold=3
    )
    config = EmailConfig(
        smtp_host="smtp.mailtrap.io",
        smtp_port=587,
        email_from="noreply@example.com",
        email_to="HysingerDev@gmail.com"
    )
    
    async with ClientSession() as session:
        result = await check_endpoint(session, endpoint, config)

    assert result.endpoint_name == "https://httpbin.org/status/200"
    assert result.success is True
    assert result.status_code == 200
    assert result.latency is not None
    assert result.error is None


