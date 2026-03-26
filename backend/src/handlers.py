from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from kinematics import calculate_wheel_speeds

router = APIRouter()


class MotionCommand(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


@router.post("/command/motion")
async def set_motion(cmd: MotionCommand, request: Request):
    left_speed, right_speed = calculate_wheel_speeds(cmd.v, cmd.omega)

    print(
        f"Motion: v={cmd.v} m/s, omega={cmd.omega} rad/s, stop={cmd.emergency_stop}")
    print(
        f"Wheel speeds: left={left_speed:.2f} rad/s, right={right_speed:.2f} rad/s")

    # TODO: write individual wheel speed commands to OPC UA
    await request.app.state.handlers_to_opc_ua.put(cmd)

    return {"status": "ok"}
