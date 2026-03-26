import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db_client import session as db_session
from opc_ua.client import session as opc_ua_session
from handlers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting background tasks...")

    app.state.to_opc_ua = asyncio.Queue()
    app.state.to_db = asyncio.Queue()

    tasks = [
        asyncio.create_task(db_session(app.state.to_db)),
        asyncio.create_task(opc_ua_session(
            incoming_commands=app.state.to_opc_ua,
            outgoing_commands=app.state.to_db,
        )),
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
