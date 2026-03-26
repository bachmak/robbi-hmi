"""Robot kinematics calculations for differential drive."""

import math
from config import robot


def calculate_wheel_speeds(v: float, omega: float) -> tuple[float, float]:
    """
    Calculate individual wheel speeds from robot linear and angular velocity.

    Args:
        v: Linear velocity (m/s)
        omega: Angular velocity (deg/s)

    Returns:
        Tuple of (left_speed, right_speed) in deg/s
    """
    wheelbase = robot.wheelbase()
    left_radius = robot.left_wheel_radius()
    right_radius = robot.right_wheel_radius()

    omega_rad = math.radians(omega)

    left_speed = math.degrees((v - omega_rad * wheelbase / 2) / left_radius)
    right_speed = -math.degrees((v + omega_rad * wheelbase / 2) / right_radius)

    return left_speed, right_speed
