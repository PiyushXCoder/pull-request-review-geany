import asyncio
import os

from schemas.reviewer import ReviewPullRequestMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import httpx
import jwt
import time

APP_ID = os.getenv("APP_ID")
with open(str(os.getenv("PRIVATE_KEY_FILE")), "r") as key_file:
    PRIVATE_KEY = key_file.read()

async def security_reviewer(queue: asyncio.Queue):
    while True:
        event = await queue.get()
        installation_token = await get_installation_token(int(event.installation_id))
        diff = await fetch_diff(installation_token, event)
        prompt = "Please review the following pull request diff for security vulnerabilities and provide feedback."
        review = await ask_gemini(prompt, diff)
        await write_comment(event, review)
        queue.task_done()


async def tidyness_reviewer(queue: asyncio.Queue):
    while True:
        event = await queue.get()
        installation_token = await get_installation_token(int(event.installation_id))
        diff = await fetch_diff(installation_token, event)
        prompt = "Please review the following pull request diff for code tidiness, style, and best practices, and provide feedback."
        review = await ask_gemini(prompt, diff)
        await write_comment(event, review)
        queue.task_done()

def create_jwt():
    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + 600,
        "iss": APP_ID,
    }

    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token

async def get_installation_token(installation_id: int):
    jwt_token = create_jwt()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers=headers
        )

    return res.json()["token"]

async def fetch_diff(token: str , pr: ReviewPullRequestMessage) -> str:
    pr_diff_url = f"https://api.github.com/repos/{pr.repo_owner}/{pr.repo_name}/pulls/{pr.pr_number}"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(
            pr_diff_url,
            headers=headers
        )
        
    return res.text 

async def write_comment(pr: ReviewPullRequestMessage, review: str):
    token = await get_installation_token(int(pr.installation_id))

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    comment_body = {
        "body": review
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.github.com/repos/{pr.repo_owner}/{pr.repo_name}/issues/{pr.pr_number}/comments",
            headers=headers,
            json=comment_body
        )
    

async def ask_gemini(prompt:str , diff: str) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = await llm.ainvoke(f"{prompt}\n\n{diff}")
    return str(response.content)
