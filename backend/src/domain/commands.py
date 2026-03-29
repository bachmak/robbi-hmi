from typing import Any, Optional
from pydantic import BaseModel


class MotorCmd(BaseModel):
    """Internal command for OPC UA motor control."""
    left_speed: float
    right_speed: float
    emergency_stop: Optional[bool] = False


class MotorPwmOverrideCmd(BaseModel):
    """Internal command for OPC UA PWM override control."""
    left_pwm: float
    right_pwm: float


class MotionIntentCmd(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


class ResendLastMotionIntentCmd(BaseModel):
    pass


class NodeMetaData(BaseModel):
    domain_name: str
    side: str
    name: str


class SaveNodeDataCmd(BaseModel):
    info: NodeMetaData
    value: Any
