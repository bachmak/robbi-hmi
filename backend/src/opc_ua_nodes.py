def _get_node_names_by_idx(idx):
    return [
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Kp"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."TargetSpeed"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Stop"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."OverridePWM"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Enable"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Fault"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."PWM"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Position"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Running"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Speed"',
        f'ns=3;s="DB_Robot"."MotorControls"[{idx}]."Motor"."Temperature"',
    ]


def get_node_names_to_subscribe():
    return _get_node_names_by_idx(0) + _get_node_names_by_idx(1)
