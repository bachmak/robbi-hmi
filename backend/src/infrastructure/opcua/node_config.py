"""OPC UA node catalog and typed builders for wheel telemetry and command nodes."""

from dataclasses import dataclass
from typing import Any

from asyncua import ua
from domain.commands import NodeMetaData


def _idx_to_side(idx):
    if idx == 0:
        return "left"
    if idx == 1:
        return "right"
    return "unknown"


def _meta_cfg(idx, name):
    return NodeMetaData(
        domain_name="wheel_config",
        side=_idx_to_side(idx),
        name=name,
    )


def _meta_state(idx, name):
    return NodeMetaData(
        domain_name="wheel_state",
        side=_idx_to_side(idx),
        name=name,
    )


def _get_leave_nodes_by_idx(idx):
    return {
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Kp"': _meta_cfg(idx, "p_coefficient"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."TargetSpeed"': _meta_state(idx, "target_speed"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Stop"': _meta_state(idx, "stop"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."OverridePWM"': _meta_state(idx, "pwm_override"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."EnableOverridePWM"': _meta_state(idx, "pwm_override_enable"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Enable"': _meta_state(idx, "enabled"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Fault"': _meta_state(idx, "fault"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."PWM"': _meta_state(idx, "pwm"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Position"': _meta_state(idx, "actual_angle"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Running"': _meta_state(idx, "operating"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Speed"': _meta_state(idx, "actual_speed"),
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Temperature"': _meta_state(idx, "temperature"),
    }


_leave_nodes = _get_leave_nodes_by_idx(0) | _get_leave_nodes_by_idx(1)


def get_leave_node_names():
    return _leave_nodes.keys()


def get_leave_node_meta_data(node):
    return _leave_nodes[node.nodeid.to_string()]


@dataclass
class NodeWithValue:
    name: str
    variant_type: ua.VariantType
    value: Any = None


class NodeWithValueBuilder:
    """Create typed write payloads for PLC nodes that accept commands from the app."""
    def left_target_speed(value: float):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[0]."TargetSpeed"', ua.VariantType.Float, value)

    def right_target_speed(value: float):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[1]."TargetSpeed"', ua.VariantType.Float, value)

    def left_stop(value: bool):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[0]."Stop"', ua.VariantType.Boolean, value)

    def right_stop(value: bool):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[1]."Stop"', ua.VariantType.Boolean, value)

    def left_pwm_override(value: float):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[0]."OverridePWM"', ua.VariantType.Float, value)

    def right_pwm_override(value: float):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[1]."OverridePWM"', ua.VariantType.Float, value)

    def left_pwm_override_enable(value: bool):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[0]."EnableOverridePWM"', ua.VariantType.Boolean, value)

    def right_pwm_override_enable(value: bool):
        return NodeWithValue(f'ns=3;s="DB_Robot"."MotorControls"[1]."EnableOverridePWM"', ua.VariantType.Boolean, value)
