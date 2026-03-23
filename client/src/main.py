import asyncio
import os
from asyncua import Client
import db
import config


class SubHandler:
    def datachange_notification(self, node, val, data):
        print(f"Value changed: {node} = {val}")


def get_url():
    ip = os.environ.get("PLC_IP", "127.0.0.1")
    return f"opc.tcp://{ip}:4840"


async def client_session(client):
    print("Connected to OPC UA Server")

    while True:
        await asyncio.sleep(1)


async def main():
    print("Connecting to OPC UA Server...")
    url = get_url()

    try:
        async with Client(url=url) as client:
            await client_session(client)
    except Exception as e:
        print(f"Could not connect to OPC UA Server: {e}, url: {url}")


if __name__ == "__main__":
    with db.create_client(
        url=config.get_db_url(),
        token=config.get_db_token(),
        org=config.get_db_org(),
    ) as db_client:
        for i in range(1, 100):
            db.write(
                client=db_client,
                bucket_name="test-bucket",
                point_name="test-measurement",
                tag_key_name="sensor",
                tag_value_name="temperature",
                field_name="value",
                value=i,
            )
