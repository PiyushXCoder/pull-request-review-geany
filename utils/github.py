import hmac
import hashlib


def verify_github_signature(secret: str, signature: str, payload: bytes) -> bool:
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)
