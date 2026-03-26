from fastapi import APIRouter, Request
from kinematics import calculate_wheel_speeds
import models

router = APIRouter()


@router.post("/command/motion")
async def set_motion(cmd: models.MotionCommand, request: Request):
    print(f"Received motion command: {cmd}")

    left_speed, right_speed = calculate_wheel_speeds(cmd.v, cmd.omega)

    await request.app.state.to_opc_ua.put(
        models.MotorCommand(
            left_speed=left_speed,
            right_speed=right_speed,
            emergency_stop=cmd.emergency_stop
        )
    )

    await request.app.state.to_db.put(
        models.MotionIntent(
            v=cmd.v,
            omega=cmd.omega,
            emergency_stop=cmd.emergency_stop,
        )
    )

    return {"status": "ok"}


@router.post("/command/pwm_override")
async def set_pwm_override(cmd: models.PwmOverrideCommand, request: Request):
    print(f"Received PWM override command: {cmd}")

    await request.app.state.to_opc_ua.put(
        models.MotorPwmOverrideCommand(
            left_pwm=cmd.left_pwm,
            right_pwm=cmd.right_pwm,
        )
    )

    return {"status": "ok"}
