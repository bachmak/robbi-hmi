import logging
from asyncua import Client
from contextlib import asynccontextmanager
from app.config import opc_ua as cfg
import asyncio
from .subscriptions import subscribe_to_leave_node_updates
from .tasks import save_leave_node_values
from .command_handlers import handle_motor_command, handle_motor_pwm_override_command
from domain.commands import MotorCommand, MotorPwmOverrideCommand

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _get_connected_client(urls):
    client = None
    for url in urls:
        client = Client(url)
        try:
            logger.info("Connecting to OPC UA server at %s...", url)
            await client.connect()
            logger.info("Connected to OPC UA server at %s", url)
            break
        except Exception as e:
            logger.info("Failed to connect to %s: %s", url, e)
            client = None
    if client is None:
        raise ConnectionError(
            "Could not connect to any OPC UA server from the list.")

    try:
        yield client
    finally:
        if client:
            await client.disconnect()
            logger.info("Disconnected from OPC UA server")


async def _init_subscriptions(
    client: Client,
    outgoing_commands: asyncio.Queue,
):
    await subscribe_to_leave_node_updates(client, outgoing_commands)


def _spawn_tasks(
    client: Client,
    outgoing_commands: asyncio.Queue,
):
    asyncio.create_task(save_leave_node_values(
        cfg.poll_interval(),
        client,
        outgoing_commands,
    ))


async def _handle_commands(
    client: Client,
    incoming_commands: asyncio.Queue,
):
    command_handlers = {
        MotorCommand: lambda cmd: handle_motor_command(cmd, client),
        MotorPwmOverrideCommand: lambda cmd: handle_motor_pwm_override_command(cmd, client),
    }

    while True:
        try:
            cmd = await incoming_commands.get()
            handler = command_handlers.get(type(cmd))
            if handler:
                await handler(cmd)
            else:
                logger.warning("Unknown command: %s", cmd)

        except Exception:
            logger.exception("Error handling command")


async def session(incoming_commands: asyncio.Queue, outgoing_commands: asyncio.Queue):
    async with _get_connected_client([
        cfg.url(),
        cfg.url_fallback(),
    ]) as client:
        await _init_subscriptions(client, outgoing_commands)
        _spawn_tasks(client, outgoing_commands)
        await _handle_commands(client, incoming_commands)
