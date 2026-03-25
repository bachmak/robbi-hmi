import asyncio
import config
import time
import math
from fastapi import FastAPI
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from fastapi.middleware.cors import CORSMiddleware
from influxdb_client import Point
from client.client import get_connected_client
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional


async def db_session():
    async with InfluxDBClientAsync(
        url=config.db.url(),
        token=config.db.token(),
        org=config.db.org(),
    ) as client:

        write_api = client.write_api()

        while True:
            value = math.sin(time.time())
            point = Point("test-measurement") \
                .tag("sensor", "temperature") \
                .field("value", value)

            await write_api.write(
                bucket=config.db.bucket_robot(),
                record=point
            )

            print(f"DB: wrote value {value}")
            await asyncio.sleep(0.1)


async def opc_ua_session():
    print("Connecting to OPC UA Server...")

    async with get_connected_client([
        config.opc_ua.url(),
        config.opc_ua.url_fallback(),
    ]) as client:

        print("Connected to OPC UA Server")

        while True:
            print("OPC UA: alive")
            await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting background tasks...")

    tasks = [
        asyncio.create_task(db_session()),
        asyncio.create_task(opc_ua_session()),
    ]

    yield

    print("Shutting down...")

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MotionCommand(BaseModel):
    v: float
    omega: float
    emergency_stop: Optional[bool] = False


@app.post("/command/motion")
async def set_motion(cmd: MotionCommand):
    print(f"v={cmd.v}, omega={cmd.omega}, stop={cmd.emergency_stop}")
    return {"status": "ok"}
