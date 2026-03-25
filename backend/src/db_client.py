from config import db as cfg
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio
from node_data import NodeData


async def session(queue: asyncio.Queue):
    async with InfluxDBClientAsync(
        url=cfg.url(),
        token=cfg.token(),
        org=cfg.org(),
    ) as client:
        write_api = client.write_api()

        while True:
            nd: NodeData = await queue.get()

            record = (
                Point(nd.info.domain_name)
                .tag("robot_id", nd.info.robot_id)
                .tag("wheel_side", nd.info.side)
                .field(nd.info.name, nd.value)
                .time(nd.ts)
            )

            await write_api.write(bucket=cfg.bucket_robot(), record=record)
