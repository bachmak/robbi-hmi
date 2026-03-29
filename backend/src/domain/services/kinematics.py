"""Robot kinematics calculations for differential drive."""

import math
from app.config import robot


def calculate_wheel_speeds(v: float, omega: float) -> tuple[float, float]:
    """Convert robot linear and angular velocity into wheel setpoints in deg/s."""
    wheelbase = robot.wheelbase()
    left_radius = robot.left_wheel_radius()
    right_radius = robot.right_wheel_radius()

    omega_rad = math.radians(omega)

    left_speed = math.degrees((v - omega_rad * wheelbase / 2) / left_radius)
    # The right wheel uses the opposite rotation sign in the OPC UA model.
    right_speed = -math.degrees((v + omega_rad * wheelbase / 2) / right_radius)

    return left_speed, right_speed
