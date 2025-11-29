from schemas.reviewer import ReviewPullRequestMessage


async def handle_pull_request_event(payload, event, queues):
    if not (event == "pull_request" and payload.get("action") in ["opened", "synchronize"]):
        return {"message": "Event ignored"}

    message = ReviewPullRequestMessage(
        installation_id=str(payload["installation"]["id"]),
        repo_owner=str(payload["repository"]["owner"]["login"]),
        repo_name=str(payload["repository"]["name"]),
        pr_number=int(payload["pull_request"]["number"]),
    )

    await queues.security_reviewer.put(message)
    await queues.tidyness_reviewer.put(message)

    return None
