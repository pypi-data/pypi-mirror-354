#-------------------- Imports --------------------

import json

from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.clockwerk.models import MonitorResult
from src.clockwerk.database import EndpointStatus
from src.clockwerk.logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Utility Functions --------------------

def create_msg(result: MonitorResult) -> str:
    """
    Summary:
        Formulates and passes the appropriate alert message based on recieved result.

    Description:
    - Recieves the appropriate information necessary to craft informative message.
    - Creates an informative alert message in JSON format.
    - Parses the JSON information into a single-string format ready to send.
    
    Args:
        result (MonitorResult): Model containing the relevant information used to craft alert message.

    Returns:
        str: Returns a single-line String-object appropriate for message sending.

    Raises:
        None
    """
    alert_msg = {
        "Endpoint": result.endpoint_name,
        "Timestamp": str(result.timestamp),
        "Status": "OUTAGE" if not result.success else "HIGH LATENCY",
        "Status code": result.status_code,
        "Latency": result.latency,
        "Error": result.error
    }
    return json.dumps(alert_msg, indent=2, sort_keys=True, ensure_ascii=True)


async def update_endpoint(session: AsyncSession, result: MonitorResult):
    status = "UP" if result.success else "DOWN"
    stmt = select(EndpointStatus).where(EndpointStatus.url == result.endpoint_name)
    res = await session.execute(stmt)
    existing = res.scalar_one_or_none()

    if existing:
        existing.current_status = status
        existing.last_updated = datetime.now(timezone.utc)
        return existing
    else:
        new_status = EndpointStatus(
            url=result.endpoint_name,
            current_status=status,
            last_updated=datetime.now(timezone.utc)
        )
        return new_status