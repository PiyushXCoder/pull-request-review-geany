import asyncio

async def security_reviewer(queue: asyncio.Queue):
    while True:
        event = await queue.get()
        # Process the event here
        print(f"security_reviewer: {event.__dict__}")
        queue.task_done()


async def tidyness_reviewer(queue: asyncio.Queue):
    while True:
        event = await queue.get()
        # Process the event here
        print(f"tidyness_reviewer: {event.__dict__}")
        queue.task_done()
