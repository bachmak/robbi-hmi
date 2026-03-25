from asyncua import Client
from contextlib import asynccontextmanager
from config import opc_ua as cfg
import asyncio
import node_cfg


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
    def datachange_notification(self, node, val, data):
        ts = data.monitored_item.Value.SourceTimestamp
        print(f"Value changed: {node} = {val}, ts = {ts}")


async def session(queue: asyncio.Queue):
    print("Connecting to OPC UA Server...")

    async with _get_connected_client([
        cfg.url(),
        cfg.url_fallback(),
    ]) as client:

        print("Connected to OPC UA Server")

        handler = SubscriptionHandler()
        subs = await client.create_subscription(
            500,
            handler,
        )

        nodes = [
            client.get_node(node_name)
            for node_name in node_cfg.get_node_names_to_subscribe()
        ]

        await subs.subscribe_data_change(nodes)

        while True:
            print("OPC UA: alive")
            await asyncio.Event().wait()
