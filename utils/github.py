from schemas.reviewer import ReviewPullRequestMessage
from utils.jwt import create_jwt
import httpx
import hmac
import hashlib


def verify_github_signature(secret: str, signature: str, payload: bytes) -> bool:
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)


async def get_installation_token(installation_id: int, app_id: str, private_key: str) -> str:
    jwt_token = create_jwt(app_id, private_key)

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


async def write_comment(pr: ReviewPullRequestMessage, review: str, token: str):
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


async def get_prefered_llm(
    pr: ReviewPullRequestMessage,
    token: str
) -> str: 
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{pr.repo_owner}/{pr.repo_name}/contents/.github/reviewer-config.json"

    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers=headers
        )
    if res.status_code == 200:
        config = res.json()
        url = config.get("download_url")

    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers=headers
        )
    if res.status_code == 200:
        config = res.json()
        llm_model = config.get("llm_model", "gemini-2.5-flash")
        return llm_model


    return "gemini-2.5-flash"
