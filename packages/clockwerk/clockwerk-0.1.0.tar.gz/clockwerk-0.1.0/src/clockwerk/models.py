#-------------------- Imports --------------------

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, AnyHttpUrl

#-------------------- Monitor Result --------------------

class MonitorResult(BaseModel):
    """
    Summary:
        Represents the result of a single monitoring check for a specified API endpoint

    Attributes:
        endpoint_name (Optional[str]): The name or identifier for the specified endpoint.
        timestamp (datetime): The time when the check was performed. Defaults to current time.
        status_code (Optional[int]): The HTTP status code recieved in the response. Defaults to 0.
        latency (Optional[float]): The round-trip time of the request in seconds.
        success (bool): Whether the response was succesfull.
        error (Optional[str]): A message describing any error that occurred during the check, if applicable.
    """
    endpoint_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    status_code: Optional[int] = 0
    latency: Optional[float] = None
    success: bool = False
    error: Optional[str] = None


class Endpoint(BaseModel):
    """
    Summary:
        Configuration for a monitored endpoint, including alert and time settings.

    Attributes:
        url (AnyHttpUrl): The full URL of the endpoint to monitor.
        timeout (int): Maximum amount of seconds to wait for a response before timing out. Defaults to 2.
        alert_threshold (int): Number of consecutive failures before raising an alert. Defaults to 3.
    """
    url: AnyHttpUrl
    timeout: int = Field(default=2, ge=1, description="The maximum number of seconds to wait for a response before considering the request timed out")
    alert_threshold: int = Field(default=3, ge=1, description="The number of consecutive failed checks before triggering an alert")


    


