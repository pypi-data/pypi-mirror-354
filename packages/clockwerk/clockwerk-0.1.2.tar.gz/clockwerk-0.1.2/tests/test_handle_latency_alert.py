import pytest
from unittest.mock import patch, AsyncMock

from src.clockwerk.reporter import handle_result
from src.clockwerk.models import MonitorResult
from src.clockwerk.reporter import send_email_alert
from src.clockwerk.config import MonitorConfig, EmailConfig, DatabaseConfig

@pytest.mark.asyncio
async def test_handle_latency_alert():

    result = MonitorResult(
        endpoint_name="https://example.com",
        latency=5.0,
        success=True,
        status_code=200
    )
    monitor_config = MonitorConfig(
        endpoints=[],
        check_interval=10,
        latency_threshold=1.0
    )
    email_config = EmailConfig(
        smtp_host="smtp.mailtrap.io",
        smtp_port=587,
        email_from="noreply@example.com",
        email_to="alert@example.com"
    )
    db_config = DatabaseConfig(
        driver_name="sqlite+aiosqlite"
    )

    with patch("src.uptime_monitor.reporter.send_email_alert", new_callable=AsyncMock) as mock:
        await handle_result(result, monitor_config, email_config, db_config)
        mock.assert_called_once()
        assert "[LATENCY ALERT]" in mock.call_args[1]["subject"]
