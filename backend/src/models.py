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


class PwmOverrideCommand(BaseModel):
    """External API request for wheel PWM override values."""
    left_pwm: float
    right_pwm: float


class MotorPwmOverrideCommand(Command):
    """Internal command for OPC UA PWM override control."""
    type: str = "motor_pwm_override"
    left_pwm: float
    right_pwm: float


class MotionIntent(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False
