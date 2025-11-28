from fastapi import APIRouter, Header, Request
import os
import hmac
import hashlib

from schemas.reviewer import ReviewPullRequestMessage


router = APIRouter()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
    print("Warning: WEBHOOK_SECRET is not set in environment variables.")
    exit(1)


def verify_github_signature(secret: str, signature: str, payload: bytes) -> bool:
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)


@router.post("/webhook")
async def webhook(request: Request,  x_hub_signature_256: str = Header(None)):
    body = await request.body()
    if not verify_github_signature(str(WEBHOOK_SECRET), x_hub_signature_256, body):
        return {"message": "Invalid signature"}, 401
    
    payload = await request.json()

    message = ReviewPullRequestMessage(
        installation_id=str(payload["installation"]["id"]),
        repo_owner=str(payload["repository"]["owner"]["login"]),
        repo_name=str(payload["repository"]["name"]),
        pr_number=int(payload["pull_request"]["number"])

    )

    await request.app.state.security_reviewer_event_queue.put(message)
    await request.app.state.tidyness_reviewer_event_queue.put(message)
    return {"message": "Webhook received"}


@router.get("/callback")
async def callback():
    return {"message": "Welcome to pull request review geany!"}

