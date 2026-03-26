from asyncua import Client, ua
from contextlib import asynccontextmanager
from config import opc_ua as cfg
import asyncio
from . import node_cfg
import node_data


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
        nd = node_data.NodeData(
            info=node_cfg.get_node_meta_data(node),
            value=val,
            ts=ts,
        )
        asyncio.create_task(self.queue.put(nd))


async def handle_commands(incoming_commands: asyncio.Queue, client: Client):
    while True:
        try:
            cmd = await incoming_commands.get()
            print(f"Received motor command: {cmd}")

            builder = node_cfg.NodeWithValueBuilder()
            node_info_with_values = [
                builder.left_target_speed(cmd.left_speed),
                builder.right_target_speed(cmd.right_speed),
                builder.left_stop(cmd.emergency_stop),
                builder.right_stop(cmd.emergency_stop),
            ]

            node_names = [node.name for node in node_info_with_values]
            nodes = [client.get_node(name) for name in node_names]
            values_to_write = [
                ua.DataValue(ua.Variant(n.value, n.variant_type))
                for n in node_info_with_values
            ]
            await client.write_values(nodes, values_to_write)

        except Exception as e:
            print(f"Error handling motor command: {e}")


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
            for node_name in node_cfg.get_node_names_to_subscribe()
        ]

        await subs.subscribe_data_change(nodes)

        command_task = asyncio.create_task(
            handle_commands(incoming_commands, client)
        )
        await asyncio.Event().wait()
