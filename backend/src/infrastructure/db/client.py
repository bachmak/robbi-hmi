import logging
from app.config import db as cfg
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import asyncio
from . import tasks
from domain.commands import MotionIntentCmd, SaveNodeDataCmd
from .command_handlers import handle_motion_intent_cmd, handle_save_node_data_cmd

logger = logging.getLogger(__name__)


async def _handle_commands(client: InfluxDBClientAsync, incoming_commands: asyncio.Queue):
    command_handlers = {
        MotionIntentCmd: lambda cmd: handle_motion_intent_cmd(cmd, client.write_api()),
        SaveNodeDataCmd: lambda cmd: handle_save_node_data_cmd(cmd, client.write_api()),
    }

    while True:
        try:
            cmd = await incoming_commands.get()
            handler = command_handlers.get(type(cmd))
            if handler:
                await handler(cmd)
            else:
                logger.warning("Unknown command: %s", cmd)

        except Exception as e:
            logger.exception("Error handling command %s", cmd)


def _spawn_tasks(client: InfluxDBClientAsync):
    write_api = client.write_api()
    query_api = client.query_api()

    asyncio.create_task(tasks.resend_last_motion_intent(
        interval=cfg.motion_resend_interval(),
        write_api=write_api,
        query_api=query_api,
    ))


async def session(incoming_commands: asyncio.Queue):
    async with InfluxDBClientAsync(
        url=cfg.url(),
        token=cfg.token(),
        org=cfg.org(),
    ) as client:
        logger.info("Connected to InfluxDB")

        _spawn_tasks(client)
        await _handle_commands(client, incoming_commands)
