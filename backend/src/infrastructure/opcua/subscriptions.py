"""Subscription bridge that forwards OPC UA data changes into internal commands."""

import logging
from asyncua import Client
import asyncio
from domain.commands import SaveNodeDataCmd
from . import node_config

logger = logging.getLogger(__name__)


class _SubscriptionHandler:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def datachange_notification(self, node, val, data):
        cmd = SaveNodeDataCmd(
            info=node_config.get_leave_node_meta_data(node),
            value=val,
        )
        # The asyncua callback is synchronous, so queue writes need to be scheduled.
        asyncio.create_task(self.queue.put(cmd))


async def subscribe_to_leave_node_updates(
        client: Client,
        outgoing_commands: asyncio.Queue,
):
    handler = _SubscriptionHandler(outgoing_commands)
    subs = await client.create_subscription(
        500,
        handler,
    )

    nodes = [
        client.get_node(node_name)
        for node_name in node_config.get_leave_node_names()
    ]

    await subs.subscribe_data_change(nodes)
    logger.info("Subscribed to %d OPC UA nodes", len(nodes))
