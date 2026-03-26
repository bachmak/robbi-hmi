"""Robot kinematics calculations for differential drive."""

from config import robot


def calculate_wheel_speeds(v: float, omega: float) -> tuple[float, float]:
    """
    Calculate individual wheel speeds from robot linear and angular velocity.

    Args:
        v: Linear velocity (m/s)
        omega: Angular velocity (rad/s)

    Returns:
        Tuple of (left_speed, right_speed) in rad/s
    """
    wheelbase = robot.wheelbase()
    left_radius = robot.left_wheel_radius()
    right_radius = robot.right_wheel_radius()

    left_speed = (v - omega * wheelbase / 2) / left_radius
    right_speed = (v + omega * wheelbase / 2) / right_radius

    return left_speed, right_speed
