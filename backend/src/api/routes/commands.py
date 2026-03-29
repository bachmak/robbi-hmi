import logging
from fastapi import APIRouter, Request
from domain.services.kinematics import calculate_wheel_speeds
from api.schemas.commands import MotionCommand, PwmOverrideCommand
from domain.commands import MotorCommand, MotionIntentCmd, MotorPwmOverrideCommand

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/command/motion")
async def set_motion(cmd: MotionCommand, request: Request):
    logger.info("Received motion command: %s", cmd)

    left_speed, right_speed = calculate_wheel_speeds(cmd.v, cmd.omega)

    await request.app.state.to_opc_ua.put(
        MotorCommand(
            left_speed=left_speed,
            right_speed=right_speed,
            emergency_stop=cmd.emergency_stop
        )
    )

    await request.app.state.to_db.put(
        MotionIntentCmd(
            v=cmd.v,
            omega=cmd.omega,
            emergency_stop=cmd.emergency_stop,
        )
    )

    return {"status": "ok"}


@router.post("/command/pwm_override")
async def set_pwm_override(cmd: PwmOverrideCommand, request: Request):
    logger.info("Received PWM override command: %s", cmd)

    await request.app.state.to_opc_ua.put(
        MotorPwmOverrideCommand(
            left_pwm=cmd.left_pwm,
            right_pwm=cmd.right_pwm,
        )
    )

    return {"status": "ok"}
