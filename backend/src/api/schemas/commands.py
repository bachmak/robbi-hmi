from pydantic import BaseModel
from typing import Optional


class MotionCommand(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


class PwmOverrideCommand(BaseModel):
    left_pwm: float
    right_pwm: float
