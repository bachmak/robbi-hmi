import logging
from asyncua import Client
import asyncio
import datetime
from domain.commands import SaveNodeDataCmd
from . import node_config

logger = logging.getLogger(__name__)


async def save_leave_node_values(
    interval: float,
    client: Client,
    queue: asyncio.Queue,
):
    nodes = [
        client.get_node(node_name)
        for node_name in node_config.get_leave_node_names()
    ]

    while True:
        try:
            values = await client.read_values(nodes)
            ts = datetime.datetime.now(datetime.timezone.utc)

            for node, val in zip(nodes, values):
                cmd = SaveNodeDataCmd(
                    info=node_config.get_leave_node_meta_data(node),
                    value=val,
                    ts=ts,
                )
                await queue.put(cmd)

        except Exception:
            logger.exception("Error saving node values")

        await asyncio.sleep(interval)
