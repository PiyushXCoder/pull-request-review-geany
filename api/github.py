from fastapi import APIRouter, Header, Request
from utils.github import verify_github_signature
from services.github import handle_pull_request_event
import env


router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request,  x_hub_signature_256: str = Header(None), x_github_event: str = Header(None)):
    body = await request.body()
    if not verify_github_signature(env.WEBHOOK_SECRET, x_hub_signature_256, body):
        return {"message": "Invalid signature"}, 401
    
    payload = await request.json()
    
    result = await handle_pull_request_event(payload, x_github_event, request.app.state.queues)
    if result is not None:
        return result

    return {"message": "Webhook received"}


@router.get("/callback")
async def callback():
    return {"message": "Welcome to pull request review geany!"}

