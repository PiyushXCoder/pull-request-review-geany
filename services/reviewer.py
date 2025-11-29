import asyncio

import env
from utils.github import get_installation_token, fetch_diff, write_comment, get_prefered_llm 
from agents.factory import AgentType, AgentFactory

async def security_reviewer(queue: asyncio.Queue):
    while True:
        try:
            pr_message = await queue.get()
            installation_token = await get_installation_token(int(pr_message.installation_id), env.APP_ID, env.PRIVATE_KEY)
            diff = await fetch_diff(installation_token, pr_message)
            llm_model = await get_prefered_llm(pr_message, installation_token)
            agent = AgentFactory.create_agent(AgentType.SECURITY_REVIEWER, llm_model)
            if agent is None:
                await write_comment(pr_message, "No suitable security reviewer agent found for this repository.", installation_token)
                queue.task_done()
                continue
            review = await agent.ask(diff)
            await write_comment(pr_message, review, installation_token)
            queue.task_done()
        except Exception as e:
            print(f"Error in security_reviewer: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            queue.task_done()


async def tidyness_reviewer(queue: asyncio.Queue):
    while True:
        try:
            pr_message = await queue.get()
            installation_token = await get_installation_token(int(pr_message.installation_id), env.APP_ID, env.PRIVATE_KEY)
            diff = await fetch_diff(installation_token, pr_message)
            llm_model = await get_prefered_llm(pr_message, installation_token)
            agent = AgentFactory.create_agent(AgentType.TIDYNESS_REVIEWER, llm_model)
            if agent is None:
                await write_comment(pr_message, "No suitable security reviewer agent found for this repository.", installation_token)
                queue.task_done()
                continue
            review = await agent.ask(diff)
            await write_comment(pr_message, review, installation_token)
            queue.task_done()
        except Exception as e:
            print(f"Error in tidyness_reviewer: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            queue.task_done()
    

