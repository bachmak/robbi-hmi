"""Data models for API requests and internal commands."""

from pydantic import BaseModel
from typing import Optional


class Command(BaseModel):
    """Base class for internal commands."""
    type: str


class MotionCommand(BaseModel):
    """External API request for robot motion control."""
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


class MotorCommand(Command):
    """Internal command for OPC UA motor control."""
    type: str = "motor"
    left_speed: float
    right_speed: float
    emergency_stop: Optional[bool] = False


class MotionIntent(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False
