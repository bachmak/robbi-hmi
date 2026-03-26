from config import db as cfg
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio
from node_data import NodeData
from models import MotionIntent


async def _write_node_data(write_api, nd: NodeData):
    record = (
        Point(nd.info.domain_name)
        .tag("wheel_side", nd.info.side)
        .field(nd.info.name, nd.value)
        # TODO: Include timestamp from OPC UA
        # .time(nd.ts)
    )
    await write_api.write(bucket=cfg.bucket_robot(), record=record)


async def _write_motion_intent(write_api, intent: MotionIntent):
    record = (
        Point("motion_intent")
        .field("v", intent.v)
        .field("omega", intent.omega)
        .field("emergency_stop", intent.emergency_stop)
    )
    await write_api.write(bucket=cfg.bucket_robot(), record=record)


async def session(incoming: asyncio.Queue):
    async with InfluxDBClientAsync(
        url=cfg.url(),
        token=cfg.token(),
        org=cfg.org(),
    ) as client:
        write_api = client.write_api()

        while True:
            event = await incoming.get()

            if isinstance(event, NodeData):
                await _write_node_data(write_api, event)
            elif isinstance(event, MotionIntent):
                await _write_motion_intent(write_api, event)
            else:
                print(f"Unknown event type: {type(event)}")
