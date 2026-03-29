import logging
from influxdb_client.client.influxdb_client_async import WriteApiAsync, QueryApiAsync
import asyncio

from domain.commands import ResendLastMotionIntentCmd
from .command_handlers import handle_resend_last_motion_intent_cmd

logger = logging.getLogger(__name__)


async def resend_last_motion_intent(
    interval: float,
    write_api: WriteApiAsync,
    query_api: QueryApiAsync,
):
    """Re-publish the last requested motion so the HMI can observe the current state at any time."""
    while True:
        try:
            await handle_resend_last_motion_intent_cmd(
                ResendLastMotionIntentCmd(),
                query_api,
                write_api
            )
        except Exception:
            logger.exception("Error re-writing motion intent")

        await asyncio.sleep(interval)
