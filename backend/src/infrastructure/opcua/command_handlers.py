"""Writers that map internal motor commands into typed OPC UA node updates."""

import logging
from asyncua import Client, ua
from . import node_config
from domain.commands import MotorCmd, MotorPwmOverrideCmd

logger = logging.getLogger(__name__)


async def handle_motor_command(
    cmd: MotorCmd,
    client: Client,
):
    builder = node_config.NodeWithValueBuilder
    node_info_with_values = [
        builder.left_target_speed(cmd.left_speed),
        builder.right_target_speed(cmd.right_speed),
        builder.left_stop(cmd.emergency_stop),
        builder.right_stop(cmd.emergency_stop),
        builder.left_pwm_override_enable(False),
        builder.right_pwm_override_enable(False),
    ]

    node_names = [node.name for node in node_info_with_values]
    nodes = [client.get_node(name) for name in node_names]
    values_to_write = [
        ua.DataValue(ua.Variant(n.value, n.variant_type))
        for n in node_info_with_values
    ]
    logger.debug(
        "Writing motor command: left_speed=%.2f, right_speed=%.2f, e_stop=%s",
        cmd.left_speed, cmd.right_speed, cmd.emergency_stop,
    )
    await client.write_values(nodes, values_to_write)


async def handle_motor_pwm_override_command(
    cmd: MotorPwmOverrideCmd,
    client: Client,
):
    builder = node_config.NodeWithValueBuilder
    node_info_with_values = [
        builder.left_pwm_override(cmd.left_pwm),
        builder.right_pwm_override(cmd.right_pwm),
        builder.left_pwm_override_enable(True),
        builder.right_pwm_override_enable(True),
    ]

    node_names = [node.name for node in node_info_with_values]
    nodes = [client.get_node(name) for name in node_names]
    values_to_write = [
        ua.DataValue(ua.Variant(n.value, n.variant_type))
        for n in node_info_with_values
    ]
    logger.debug(
        "Writing PWM override: left_pwm=%.2f, right_pwm=%.2f",
        cmd.left_pwm, cmd.right_pwm,
    )
    await client.write_values(nodes, values_to_write)
