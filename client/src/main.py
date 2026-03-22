import asyncio
import os
from asyncua import Client

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
    asyncio.run(main())

