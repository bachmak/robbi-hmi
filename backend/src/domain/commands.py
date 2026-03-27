import datetime
from typing import Any
from pydantic import BaseModel
from typing import Optional


class Command(BaseModel):
    """Base class for internal commands."""
    type: str


class MotorCommand(Command):
    """Internal command for OPC UA motor control."""
    type: str = "motor"
    left_speed: float
    right_speed: float
    emergency_stop: Optional[bool] = False


class MotorPwmOverrideCommand(Command):
    """Internal command for OPC UA PWM override control."""
    type: str = "motor_pwm_override"
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
    ts: datetime.datetime
