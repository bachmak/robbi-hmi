from fastapi import APIRouter, Request
from kinematics import calculate_wheel_speeds
from models import MotionCommand, MotorCommand, MotionIntent

router = APIRouter()


@router.post("/command/motion")
async def set_motion(cmd: MotionCommand, request: Request):
    print(f"Received command: {cmd}")

    left_speed, right_speed = calculate_wheel_speeds(cmd.v, cmd.omega)

    await request.app.state.to_opc_ua.put(
        MotorCommand(
            left_speed=left_speed,
            right_speed=right_speed,
            emergency_stop=cmd.emergency_stop
        )
    )

    await request.app.state.to_db.put(
        MotionIntent(
            v=cmd.v,
            omega=cmd.omega,
            emergency_stop=cmd.emergency_stop,
        )
    )

    return {"status": "ok"}
