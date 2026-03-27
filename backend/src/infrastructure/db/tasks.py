from influxdb_client.client.influxdb_client_async import WriteApiAsync, QueryApiAsync
import asyncio

from domain.commands import ResendLastMotionIntentCmd
from .command_handlers import handle_resend_last_motion_intent_cmd


async def resend_last_motion_intent(
    interval: float,
    write_api: WriteApiAsync,
    query_api: QueryApiAsync,
):
    while True:
        try:
            await handle_resend_last_motion_intent_cmd(
                ResendLastMotionIntentCmd(),
                query_api,
                write_api
            )
        except Exception as e:
            print(f"Error re-writing motion intent: {e}")

        await asyncio.sleep(interval)
