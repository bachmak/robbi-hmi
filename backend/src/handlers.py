from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class MotionCommand(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


@router.post("/command/motion")
async def set_motion(cmd: MotionCommand):
    print(f"v={cmd.v}, omega={cmd.omega}, stop={cmd.emergency_stop}")
    return {"status": "ok"}
