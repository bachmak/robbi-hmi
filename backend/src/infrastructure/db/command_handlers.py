import logging
from influxdb_client import Point
from app.config import db as cfg
from domain.commands import SaveNodeDataCmd, MotionIntentCmd, ResendLastMotionIntentCmd
from influxdb_client.client.influxdb_client_async import WriteApiAsync, QueryApiAsync
from . import queries

logger = logging.getLogger(__name__)


async def handle_save_node_data_cmd(
    command: SaveNodeDataCmd,
    write_api: WriteApiAsync,
):
    record = (
        Point(command.info.domain_name)
        .tag("wheel_side", command.info.side)
        .field(command.info.name, command.value)
    )
    await write_api.write(bucket=cfg.bucket_robot(), record=record)


async def handle_motion_intent_cmd(
    command: MotionIntentCmd,
    write_api: WriteApiAsync,
):
    record = (
        Point("motion_intent")
        .field("v", command.v)
        .field("omega", command.omega)
        .field("emergency_stop", command.emergency_stop)
    )
    await write_api.write(bucket=cfg.bucket_robot(), record=record)


async def handle_resend_last_motion_intent_cmd(
    _: ResendLastMotionIntentCmd,
    query_api: QueryApiAsync,
    write_api: WriteApiAsync
):
    intent = await queries.query_last_motion_intent(query_api)
    if intent:
        await handle_motion_intent_cmd(intent, write_api)
    else:
        logger.warning("No initial motion intent found in DB.")
