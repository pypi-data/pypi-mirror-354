#-------------------- Imports --------------------

import asyncio
import aiohttp

from src.clockwerk.monitor import check_endpoint
from src.clockwerk.reporter import handle_result
from src.clockwerk.config import EmailConfig, MonitorConfig, DatabaseConfig
from src.clockwerk.database import init_database
from src.clockwerk.logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Scheduler Function --------------------

async def scheduling_loop(monitor_config: MonitorConfig, email_config: EmailConfig, db_config: DatabaseConfig):
    """
    Summary:
    Runs an asynchronous monitoring loop that periodically checks endpoints and handles results.
    
    Description:
    - Initializes DB if enabled by user.
    - Iterates over all endpoints in the monitor configuration.
    - Checks each endpoint asynchronously.
    - Handles results including alerts and database updates.
    - Waits for the configured interval before repeating.
    - Cleans up resources, including shutting down the database engine on cancellation.

    Args:
        monitor_config (MonitorConfig): Configuration model containing Endpoints list, check interval & latency threshold
        email_config (EmailConfig): Configuration model containing SMTP Host, SMTP Port, recieving E-mail and sending E-mail
        db_config (DatabaseConfig): Configuration model containing available drivers, DB activation flag, and other DB config variables

    Returns:
        None

    Raises:
        Asyncio.CancelledError: Raised when the loop is cancelled, initiating cleanup

    """

    engine = None
    sessionmaker = None

    if db_config.db_activation:
        sessionmaker, engine = await init_database(db_config)

    try:
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [
                    check_endpoint(session=session, endpoint=ep, email_config=email_config)
                    for ep in monitor_config.endpoints
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                await asyncio.gather(*(
                    handle_result(result, monitor_config, email_config, db_config, sessionmaker)
                    for result in results
                ))
                logger.info("All Endpoints have been checked and appropriate measures taken!")
                
                await asyncio.sleep(monitor_config.check_interval)
                logger.info(f"Scheduling loop returning to sleep for {monitor_config.check_interval} seconds")
    except asyncio.CancelledError:
        logger.info(f"Scheduling loop is shutting down...")
    finally:
        if engine:
            await engine.dispose()
        logger.info(f"Scheduling loop cleanup is complete")