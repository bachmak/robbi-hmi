import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import db_client
import opc_ua_client
from handlers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting background tasks...")

    tasks = [
        asyncio.create_task(db_client.session()),
        asyncio.create_task(opc_ua_client.session()),
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

app.include_router(router)
