"""Domain command models passed between API, OPC UA, and database layers."""

from typing import Any, Optional
from pydantic import BaseModel


class MotorCmd(BaseModel):
    """Wheel speed setpoint sent to the OPC UA layer."""
    left_speed: float
    right_speed: float
    emergency_stop: Optional[bool] = False


class MotorPwmOverrideCmd(BaseModel):
    """Direct wheel PWM values sent to the OPC UA layer."""
    left_pwm: float
    right_pwm: float


class MotionIntentCmd(BaseModel):
    """Requested robot motion stored for replay and observability."""
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


class ResendLastMotionIntentCmd(BaseModel):
    """Marker command that republishes the latest stored motion intent."""
    pass


class NodeMetaData(BaseModel):
    """Measurement and field metadata associated with a sampled node."""
    domain_name: str
    side: str
    name: str


class SaveNodeDataCmd(BaseModel):
    """Write a node sample to the time-series database."""
    info: NodeMetaData
    value: Any
