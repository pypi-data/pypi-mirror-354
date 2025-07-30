#-------------------- Imports --------------------

import aiosmtplib

from email.message import EmailMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.clockwerk.utils import create_msg
from src.clockwerk.utils import write_to_db
from src.clockwerk.models import MonitorResult
from src.clockwerk.config import EmailConfig, MonitorConfig, DatabaseConfig
from src.clockwerk.logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Reporting Function --------------------

async def handle_result(
        result: MonitorResult,
        monitor_config: MonitorConfig,
        email_config: EmailConfig,
        db_config: DatabaseConfig,
        sessionmaker: Optional[async_sessionmaker] = None
    ):
    """
    Summary:
    Reports the monitoring result to the specified e-mail outlet and database

    Description:
    - Recieves a MonitorResult-object from individual endpoints
    - Writes the appropriate information to DB (Requires DB-connection enabled)
    - Formulates a standardized alert message based on status-response or latency
    - Raises an e-mail alert to the appropriate outlet.

    Args:
        result (MonitorResult): MonitorResult-object used for creating e-mail response
        monitor_config (MonitorConfig): Configuration model containing Endpoints list, check interval & latency threshold
        email_config (EmailConfig): Configuration model containing SMTP Host, SMTP Port, recieving E-mail and sending E-mail
        db_config (DatabaseConfig): Configuration model containing available drivers, DB activation flag, and other DB config variables

    Returns:
        None

    Raises:
        Exception: Raised if the e-mail alert was not succesfully sent.
    """

    # Step 1: Write to DB is activation is enabled
    if db_config.db_activation and sessionmaker:
        await write_to_db(result, sessionmaker)

    # Step 2: Write the appopriate Alert messages

    try:
        if not result.success:
            alert_subject = f"[OUTAGE ALERT] - {result.endpoint_name} is experiencing an outage"
            alert_msg = create_msg(result=result)
            await send_email_alert(
                message=alert_msg,
                subject=alert_subject,
                email_config=email_config
            )
            logger.info("Outage message sent!")
        elif result.latency >= monitor_config.latency_threshold:
            alert_subject = f"[LATENCY ALERT] - {result.endpoint_name} is experiencing latency"
            alert_msg = create_msg(result=result)
            await send_email_alert(
                message=alert_msg,
                subject=alert_subject,
                email_config=email_config
            )
            logger.info("Latency message sent!")
    except Exception as err:
        logger.error(f"Critical: Latency e-mail could not be sent: {err}")


@retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((aiosmtplib.SMTPException))
)
async def send_email_alert(message: str, subject: str, email_config: EmailConfig):
    email_msg = EmailMessage()
    email_msg["From"] = email_config.email_from
    email_msg["To"] = email_config.email_to
    email_msg["Subject"] = subject
    email_msg.set_content(message)
    
    try:
        response = await aiosmtplib.send(
            email_msg, hostname=email_config.smtp_host, port=email_config.smtp_port
        )
        if response[0].code != 250:
            raise Exception("SMTP not accepted")
    except aiosmtplib.SMTPException as err:
        logger.exception(f"Failed to send the email: {err}")

