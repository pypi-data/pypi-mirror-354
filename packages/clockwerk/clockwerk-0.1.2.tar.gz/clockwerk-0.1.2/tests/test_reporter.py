import pytest_asyncio
import pytest
from unittest.mock import patch, AsyncMock

from src.clockwerk.reporter import send_email_alert
from src.clockwerk.config import EmailConfig

@pytest.mark.asyncio
async def test_send_email_alert():
    email_config = EmailConfig(
        smtp_host="smtp.mailtrap.io",
        smtp_port=587,
        email_from="noreply@example.com",
        email_to="noreply2@example.com"
    )
    subject = f"[SUBJECT] - Testing e-mail alert system"
    message = f"Test email sent from {email_config.email_from} to {email_config.email_to}"

    # Create Mock methods
    with patch("src.uptime_monitor.reporter.aiosmtplib.send", new_callable=AsyncMock) as mock_send:
        mock_response = type("SMTPresponse", (), {"code": 250})()
        mock_send.return_value = (mock_response, None)

        await send_email_alert(
            subject=subject,
            message=message,
            email_config=email_config
        )

        mock_send.assert_called_once()
        called_msg = mock_send.call_args[0][0]

        assert called_msg["From"] == email_config.email_from
        assert called_msg["To"] == email_config.email_to
        assert called_msg["Subject"] == subject