from asyncua import Client, ua
from contextlib import asynccontextmanager
from app.config import opc_ua as cfg
import asyncio
from . import node_config
from domain.commands import SaveNodeDataCmd
import datetime


@asynccontextmanager
async def _get_connected_client(urls):
    client = None
    for url in urls:
        client = Client(url)
        try:
            print(f"Connecting to OPC UA server at {url}...")
            await client.connect()
            print(f"Connected")
            break
        except Exception as e:
            print(f"Failed to connect: {e}")
            client = None
    if client is None:
        raise ConnectionError(
            "Could not connect to any OPC UA server from the list.")

    try:
        yield client
    finally:
        if client:
            await client.disconnect()
            print("Disconnected from OPC UA server")


class SubscriptionHandler:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def datachange_notification(self, node, val, data):
        ts = data.monitored_item.Value.SourceTimestamp
        cmd = SaveNodeDataCmd(
            info=node_config.get_node_meta_data(node),
            value=val,
            ts=ts,
        )
        asyncio.create_task(self.queue.put(cmd))


async def _poll_node_values(client: Client, nodes, queue: asyncio.Queue):
    poll_interval = cfg.poll_interval()

    while True:
        try:
            values = await client.read_values(nodes)
            ts = datetime.datetime.now(datetime.timezone.utc)

            for node, val in zip(nodes, values):
                try:
                    cmd = SaveNodeDataCmd(
                        info=node_config.get_node_meta_data(node),
                        value=val,
                        ts=ts,
                    )
                    await queue.put(cmd)
                except Exception as e:
                    print(f"Error processing node {node.nodeid}: {e}")

            await asyncio.sleep(poll_interval)
        except Exception as e:
            print(f"Error in node polling task: {e}")
            await asyncio.sleep(poll_interval)


async def _handle_commands(incoming_commands: asyncio.Queue, client: Client):
    command_handlers = {
        "motor": _handle_motor_command,
        "motor_pwm_override": _handle_motor_pwm_override_command,
    }

    while True:
        try:
            cmd = await incoming_commands.get()
            print(f"Received command: {cmd}")

            handler = command_handlers.get(cmd.type)
            if handler:
                await handler(cmd, client)
            else:
                print(f"Unknown command type: {cmd.type}")

        except Exception as e:
            print(f"Error handling command: {e}")


async def _handle_motor_command(cmd, client: Client):
    builder = node_config.NodeWithValueBuilder
    node_info_with_values = [
        builder.left_target_speed(cmd.left_speed),
        builder.right_target_speed(cmd.right_speed),
        builder.left_stop(cmd.emergency_stop),
        builder.right_stop(cmd.emergency_stop),
        builder.left_pwm_override_enable(False),
        builder.right_pwm_override_enable(False),
    ]

    node_names = [node.name for node in node_info_with_values]
    nodes = [client.get_node(name) for name in node_names]
    values_to_write = [
        ua.DataValue(ua.Variant(n.value, n.variant_type))
        for n in node_info_with_values
    ]
    await client.write_values(nodes, values_to_write)


async def _handle_motor_pwm_override_command(cmd, client: Client):
    builder = node_config.NodeWithValueBuilder
    node_info_with_values = [
        builder.left_pwm_override(cmd.left_pwm),
        builder.right_pwm_override(cmd.right_pwm),
        builder.left_pwm_override_enable(True),
        builder.right_pwm_override_enable(True),
    ]

    node_names = [node.name for node in node_info_with_values]
    nodes = [client.get_node(name) for name in node_names]
    values_to_write = [
        ua.DataValue(ua.Variant(n.value, n.variant_type))
        for n in node_info_with_values
    ]
    await client.write_values(nodes, values_to_write)


async def session(incoming_commands: asyncio.Queue, outgoing_commands: asyncio.Queue):
    print("Connecting to OPC UA Server...")

    async with _get_connected_client([
        cfg.url(),
        cfg.url_fallback(),
    ]) as client:

        print("Connected to OPC UA Server")

        handler = SubscriptionHandler(outgoing_commands)
        subs = await client.create_subscription(
            500,
            handler,
        )

        nodes = [
            client.get_node(node_name)
            for node_name in node_config.get_node_names_to_subscribe()
        ]

        await subs.subscribe_data_change(nodes)

        asyncio.create_task(
            _handle_commands(incoming_commands, client)
        )
        asyncio.create_task(
            _poll_node_values(client, nodes, outgoing_commands)
        )
        await asyncio.Event().wait()
