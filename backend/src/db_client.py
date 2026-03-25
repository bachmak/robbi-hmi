from config import db as cfg
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio
import math
import time


async def session():
    async with InfluxDBClientAsync(
        url=cfg.url(),
        token=cfg.token(),
        org=cfg.org(),
    ) as client:

        write_api = client.write_api()

        while True:
            value = math.sin(time.time())
            point = Point("test-measurement") \
                .tag("sensor", "temperature") \
                .field("value", value)

            await write_api.write(
                bucket=cfg.bucket_robot(),
                record=point
            )

            print(f"DB: wrote value {value}")
            await asyncio.sleep(0.1)
