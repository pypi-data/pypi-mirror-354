#-------------------- Imports --------------------

from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

#-------------------- Database Schemas --------------------

class Base(DeclarativeBase):
    pass


class EndpointStatus(Base):
    """
    Summary:
        Represents the current status of a monitored endpoint.

    Attributes:
        id (Mapped[int]): Primary key identifier for the record.
        url (MMApped[str]): The unique URL of the monitored endpoint.
        current_status (MApped[str]): The current status of the monitored endpoint.
        last_updated (Mapped[datetime]): UTC timestamp of when the endpoint was last updated.
    """
    __tablename__ = "endpoint_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2083), unique=True, nullable=False)
    current_status: Mapped[str] = mapped_column(String(50), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class MonitorHistory(Base):
    """
    Summary:
        Stores the historical record of individual endpoints over time.

    Attributes:
        id (Mapped[int]): Primary key identifier for the record.
        url (Mapped[str]): The unique URL of the monitored endpoint.
        timestamp (Mapped[datetime]): UTC timestamp of when the historical record was initialised.
        status_code (Mapped[int]): The HTTP status code recieved during the check.
        latency (Mapped[float]): The request-to-response time represented in seconds.
        success (Mapped[bool]): Indicates whether the endpoint check succeeded.
        error (Mapped[str]): A description of any recieved errors encountered during checks.
    """
    __tablename__ = "monitor_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2083), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    status_code: Mapped[int] = mapped_column(nullable=False)
    latency: Mapped[float] = mapped_column(nullable=False)
    success: Mapped[bool] = mapped_column(default=True)
    error: Mapped[str] = mapped_column(String(255), nullable=True)




