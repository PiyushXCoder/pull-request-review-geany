#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api import github
import asyncio
from services.reviewer import security_reviewer, tidyness_reviewer


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.security_reviewer_event_queue = asyncio.Queue()
    app.state.tidyness_reviewer_event_queue = asyncio.Queue()
    app.state.security_reviewer_worker_task = asyncio.create_task(security_reviewer(app.state.security_reviewer_event_queue))
    app.state.tidyness_reviewer_worker_task = asyncio.create_task(tidyness_reviewer(app.state.tidyness_reviewer_event_queue))

    yield  

    # Shutdown
    app.state.security_reviewer_worker_task.cancel()
    app.state.tidyness_reviewer_worker_task.cancel()
    await asyncio.sleep(0)  

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health_check():
    return {"message": "Welcome to pull resuest review geany!"}


app.include_router(github.router)

