import logging
from app.config import db as cfg
from domain.commands import MotionIntentCmd

logger = logging.getLogger(__name__)


async def query_last_motion_intent(query_api) -> MotionIntentCmd | None:
    try:
        query = f'''
            from(bucket: "{cfg.bucket_robot()}")
            |> range(start: -30d)
            |> filter(fn: (r) => r._measurement == "motion_intent")
            |> last()
            |> pivot(
                rowKey:["_time"],
                columnKey: ["_field"],
                valueColumn: "_value"
            )
        '''
        tables = await query_api.query(query)

        for table in tables:
            for record in table.records:
                return MotionIntentCmd(
                    v=float(record["v"]),
                    omega=float(record["omega"]),
                    emergency_stop=bool(record["emergency_stop"]),
                )
    except Exception:
        logger.exception("Error querying last motion intent")

    return None
