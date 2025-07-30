#-------------------- Imports --------------------

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.clockwerk.models import MonitorResult
from src.clockwerk.database import get_session
from src.clockwerk.database import MonitorHistory
from src.clockwerk.utils import update_endpoint
from src.clockwerk.logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Utility Functions --------------------

async def write_to_db(result: MonitorResult, sessionmaker: async_sessionmaker):
    """
    Summary:
        Writes the specified result-object to database

    Description:
    - Recives MonitorResult-object and sessionmaker.
    - Utilises sessionmaker-object to instantialize an async database session.
    - Waits for the resulting information to be commited to database.
    - Handles cleanup of the asynnchronous database session.

    Args:
        result (MonitorResult): Model containing relevant information regarding the last endpoint check.
        sessionmaker (async_sessionmaker): Asynchronous sessionmaker used for providing a SQLalchemy session. 

    Raises:
        SQLalchemyError: Raised if session was unsuccessfull in wiritng result to database.

    Returns:
        None
    """
    async with get_session(sessionmaker) as session:
        try:
            history_entry = MonitorHistory(
                url=result.endpoint_name,
                timestamp=result.timestamp,
                status_code=result.status_code,
                latency=result.latency,
                success=result.success,
                error=result.error
            )
            session.add(history_entry)
            endpoint_status = await update_endpoint(session, result)
            session.add(endpoint_status)

            await session.commit()
        except SQLAlchemyError or Exception as err:
            await session.rollback()
            logger.exception(f"Database operation failed: {err}")
        finally:
            await session.close()