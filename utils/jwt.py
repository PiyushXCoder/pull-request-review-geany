import time
import jwt


def create_jwt(app_id, private_key):
    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + 600,
        "iss": app_id,
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token
