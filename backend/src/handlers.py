from fastapi import APIRouter, Request
from kinematics import calculate_wheel_speeds
from models import MotionCommand, MotorCommand

router = APIRouter()


@router.post("/command/motion")
async def set_motion(cmd: MotionCommand, request: Request):
    print(f"Received command: {cmd}")

    left_speed, right_speed = calculate_wheel_speeds(cmd.v, cmd.omega)

    motor_cmd = MotorCommand(
        left_speed=left_speed,
        right_speed=right_speed,
        emergency_stop=cmd.emergency_stop
    )
    await request.app.state.handlers_to_opc_ua.put(motor_cmd)

    return {"status": "ok"}
