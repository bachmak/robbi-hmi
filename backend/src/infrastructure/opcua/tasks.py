"""Polling tasks that sample OPC UA node values and enqueue telemetry commands."""

import logging
from asyncua import Client
import asyncio
from domain.commands import SaveNodeDataCmd
from . import node_config

logger = logging.getLogger(__name__)


async def save_leave_node_values(
    interval: float,
    client: Client,
    queue: asyncio.Queue,
):
    """Periodically poll tracked PLC nodes and forward the samples to the DB queue.
      This is a simple workaround to ensure there is data to show in the UI even
      if OPC UA values only change sporadically."""
    nodes = [
        client.get_node(node_name)
        for node_name in node_config.get_leave_node_names()
    ]

    while True:
        try:
            values = await client.read_values(nodes)

            for node, val in zip(nodes, values):
                cmd = SaveNodeDataCmd(
                    info=node_config.get_leave_node_meta_data(node),
                    value=val,
                )
                await queue.put(cmd)

        except Exception:
            logger.exception("Error saving node values")

        await asyncio.sleep(interval)
