import asyncio
import config
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client import Point

from client.client import get_connected_client


class SubHandler:
    def datachange_notification(self, node, val, data):
        print(f"Value changed: {node} = {val}")


async def db_session():
    async with InfluxDBClientAsync(
        url=config.db.url(),
        token=config.db.token(),
            org=config.db.org(),
    ) as client:
        for i in range(1, 100):
            point = Point("test-measurement") \
                .tag("sensor", "temperature") \
                .field("value", i)
            await client.write_api().write(bucket=config.db.bucket_robot(), record=point)
            print("DB: sleeep....")
            await asyncio.sleep(1)


async def opc_ua_session():
    print("Connecting to OPC UA Server...")
    async with get_connected_client([
        config.opc_ua.url(),
        config.opc_ua.url_fallback(),
    ]) as client:
        print("Connected to OPC UA Server")

        while True:
            print("OPC UA: sleeep....")
            await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        db_session(),
        opc_ua_session(),
    )


if __name__ == "__main__":
    asyncio.run(main())
