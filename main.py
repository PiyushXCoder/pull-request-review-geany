#!/usr/bin/env python3

from fastapi.responses import FileResponse
import env # Ensure environment variables are loaded

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api import github
import asyncio
from services.reviewer import security_reviewer, tidyness_reviewer
from types import SimpleNamespace


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.queues = SimpleNamespace(
        security_reviewer=asyncio.Queue(),
        tidyness_reviewer=asyncio.Queue(),
    )
    app.state.worker_tasks = SimpleNamespace(
        security_reviewer=None,
        tidyness_reviewer=None,
    )
    app.state.worker_tasks.security_reviewer = asyncio.create_task(security_reviewer(app.state.queues.security_reviewer))
    app.state.worker_tasks.tidyness_reviewer = asyncio.create_task(tidyness_reviewer(app.state.queues.tidyness_reviewer))

    yield  

    # Shutdown
    app.state.worker_tasks.security_reviewer.cancel()
    app.state.worker_tasks.tidyness_reviewer.cancel()
    await asyncio.sleep(0)  

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health_check():
    return FileResponse("views/index.html")

@app.get("/logo.png")
async def logo():
    return FileResponse("logo.png")


app.include_router(github.router)

