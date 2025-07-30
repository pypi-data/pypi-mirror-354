#-------------------- Imports --------------------

from typing import Optional, Literal, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator, EmailStr

from src.clockwerk.models import Endpoint

#-------------------- Config Models --------------------

class LoggerConfig(BaseModel):
    """
    Summary:
        Configuration model for loggin information in the monitoring application.
     
    Attributes:
        log_level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]): 
            Minimum severity level of log messages to capture. Defaults to 'INFO'.
        log_file (str): 
            Path to the log file where logs are stored. Default to 'Monitor.log'.
        log_to_fiel (bool): 
            Determines if the log should write to file. Defaults to True.
        log_format (str):
            Format strings for log messages.
        date_format (str): 
            Format strings for timestamps in log messages.
    """
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: str = Field(default="monitor.log")
    log_to_file: bool = Field(default=True)
    log_format: str = Field(default="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S")


class EmailConfig(BaseModel):
    """
    Summary:
        Configuration model for email settings.
    
    Attributes:
        smtp_host (str):
            Hostname of the SMTP server used to send emails.
        smtp_port (int):
            Port number fo the SMTP server. Must be between 1 - 65535. Defaults to 587.
        email_from (EmailStr):
            Sender's email address used in alert messages.
        email_to (EmailStr):
            Recipient's email address used to receive alert notifications.
    """
    smtp_host: str = Field(default="smtp.mailtrap.io")
    smtp_port: int = Field(default=587, ge=1, le=65535)
    email_from: EmailStr
    email_to: EmailStr


class MonitorConfig(BaseModel):
    """
    Summary:
        Configuration model for uptime and latency monitoring settings.
    
    Attributes:
        endpoints (List[Ednpoint]):
            List of Endpoint objects to be monitored.
        check_interval (int):
            Interval in seconds between endpoint checks. Must be at least 5 seconds. Defaults to 60.
        latency_threshold (float):
            Maximum latency in seconds before triggering an alert notification. Defaults to 1.5.
    """
    endpoints: List[Endpoint] = Field(default_factory=list)
    check_interval: int = Field(default=60, ge=5, description="Interval between Uptime checks")
    latency_threshold: float = Field(default=1.5, ge=0.5, description="Max acceptable latency in seconds")
    

class SupportedDrivers(str, Enum):
    """
    Summary:
        Database drivers currently supported for connectivity and querying (ENUM).
    
    Enum Members:
        mysql: MySQL driver using mysqlconnector.
        postgresql: Postgressql driver using asyncpg.
        sqlite: SQLite driver using aiosqlite.
    """
    mysql = "mysql+mysqlconnector"
    postgresql = "postgresql+asyncpg"
    sqlite = "sqlite+aiosqlite"


class DatabaseConfig(BaseModel):
    """
    Summary:
        Configuration model for database connection settings.

    Attributes:
        driver_name (SuppertedDrivers): 
            The database driver to use for establishing a connection.
        db_host_name (Optional[str]): 
            Hostname or IP address of the database server.
        db_username (Optional[str]): 
            Username for authentication within the database.
        db_name (Optional[str]): 
            Current identifying name of the database to connect to.
        db_password (Optional[str]): 
            Database user's personal password.
        db_port (Optional[int]): 
            Port number on which the database is listening. Defaults to 5437.
        db_activation (bool): 
            If True, enables database interaction and functionality.
        echo_mode (bool): 
            If True, enables sqlalchemy's echo moder for verbose query logging (Debugging Tool).
    """
    driver_name: SupportedDrivers
    db_host_name: Optional[str] = None
    db_username: Optional[str] = None
    db_name: Optional[str] = None
    db_password: Optional[str] = None
    db_port: Optional[int] = 5437
    db_activation: bool = False
    echo_mode: bool = False