from config import db as cfg
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio
import math
import time
import random


async def session():
    async with InfluxDBClientAsync(
        url=cfg.url(),
        token=cfg.token(),
        org=cfg.org(),
    ) as client:

        write_api = client.write_api()

        while True:
            timestamp = int(time.time() * 1_000_000_000)  # Nanoseconds

            for wheel_side in ["left", "right"]:
                target_speed = random.uniform(0, 2)       # m/s
                actual_speed = target_speed + random.uniform(-0.1, 0.1)
                target_angle = random.uniform(-0.5, 0.5)  # rad
                actual_angle = target_angle + random.uniform(-0.05, 0.05)
                pwm = random.randint(0, 255)
                temperature = random.uniform(30, 40)

                p_coefficient = 2.5
                alpha_coefficient = 0.8

                point_state = (
                    Point("wheel_state")
                    .tag("robot_id", "robot1")
                    .tag("wheel_side", wheel_side)
                    .field("target_speed", target_speed)
                    .field("actual_speed", actual_speed)
                    .field("target_angle", target_angle)
                    .field("actual_angle", actual_angle)
                    .field("pwm", pwm)
                    .field("temperature", temperature)
                    .time(timestamp)
                )

                point_config = (
                    Point("wheel_config")
                    .tag("robot_id", "robot1")
                    .tag("wheel_side", wheel_side)
                    .field("p_coefficient", p_coefficient)
                    .field("alpha_coefficient", alpha_coefficient)
                    .time(timestamp)
                )

                await write_api.write(bucket=cfg.bucket_robot(), record=point_state)
                await write_api.write(bucket=cfg.bucket_robot(), record=point_config)

                print(f"[{wheel_side}] wrote state and config at {time.time()}")

            await asyncio.sleep(0.1)  # 10 Hz
