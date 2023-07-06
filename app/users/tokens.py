from itsdangerous import URLSafeTimedSerializer

from config import get_settings


def generate_token(email):
    secret_key = get_settings().SECRET_KEY
    serializer = URLSafeTimedSerializer(secret_key=secret_key)
    return serializer.dumps(email)


def confirm_token(token, expiration=3600):
    secret_key = get_settings().SECRET_KEY
    serializer = URLSafeTimedSerializer(secret_key=secret_key)
    try:
        email = serializer.loads(
            token, max_age=expiration
        )
        return email
    except Exception:
        return False
