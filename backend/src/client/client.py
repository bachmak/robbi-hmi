from asyncua import Client
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_connected_client(urls):
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
