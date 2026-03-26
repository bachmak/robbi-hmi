"""Data models for API requests and internal commands."""

from pydantic import BaseModel
from typing import Optional


class MotionCommand(BaseModel):
    """External API request for robot motion control."""
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


class MotorCommand(BaseModel):
    """Internal command for OPC UA motor control."""
    left_speed: float
    right_speed: float
    emergency_stop: Optional[bool] = False
