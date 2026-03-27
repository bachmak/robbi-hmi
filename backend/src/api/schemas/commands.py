"""API request models."""

from pydantic import BaseModel
from typing import Optional


class MotionCommand(BaseModel):
    """External API request for robot motion control."""
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


class PwmOverrideCommand(BaseModel):
    """External API request for wheel PWM override values."""
    left_pwm: float
    right_pwm: float
