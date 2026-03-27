from app.config import db as cfg
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio
from domain.node_data import NodeData
from domain.commands import MotionIntent


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


async def _get_last_motion_intent(query_api):
    try:
        query = f'''
            from(bucket: "{cfg.bucket_robot()}")
            |> range(start: -30d)
            |> filter(fn: (r) => r._measurement == "motion_intent")
            |> last()
        '''
        tables = await query_api.query(query)

        if tables and len(tables) > 0 and len(tables[0].records) > 0:
            record = tables[0].records[0]
            values = record.values
            return MotionIntent(
                v=values.get("v", 0.0),
                omega=values.get("omega", 0.0),
                emergency_stop=values.get("emergency_stop", False),
            )
    except Exception as e:
        print(f"Error querying last motion intent: {e}")

    return None


async def _resend_last_motion_intent(write_api, last_intent):
    """Periodically re-write the last motion intent with current timestamp."""
    resend_interval = cfg.motion_resend_interval()

    while True:
        await asyncio.sleep(resend_interval)

        if last_intent[0] is not None:
            try:
                await _write_motion_intent(write_api, last_intent[0])
                print(
                    f"Re-wrote motion intent to DB: v={last_intent[0].v}, omega={last_intent[0].omega}")
            except Exception as e:
                print(f"Error re-writing motion intent: {e}")


async def session(incoming: asyncio.Queue):
    async with InfluxDBClientAsync(
        url=cfg.url(),
        token=cfg.token(),
        org=cfg.org(),
    ) as client:
        write_api = client.write_api()
        query_api = client.query_api()

        # Use a mutable container so the resend task sees updates
        last_intent = [None]

        initial_intent = await _get_last_motion_intent(query_api)
        if initial_intent:
            last_intent[0] = initial_intent

        asyncio.create_task(_resend_last_motion_intent(write_api, last_intent))

        while True:
            event = await incoming.get()

            if isinstance(event, NodeData):
                await _write_node_data(write_api, event)
            elif isinstance(event, MotionIntent):
                last_intent[0] = event
                await _write_motion_intent(write_api, event)
            else:
                print(f"Unknown event type: {type(event)}")
