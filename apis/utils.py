from django.http import JsonResponse
from json import loads
from jwt import encode, decode
from django.conf import settings
from datetime import datetime, timezone, timedelta
from .models import User

SUCCESS = "success"
ERROR = "error"


def parse_body(body):
    return loads(body.decode("utf-8"))


def get_success_response(data=None):
    return JsonResponse(
        {
            "status": SUCCESS,
            "data": data,
            "error": None,
        }
    )


def get_error_response(error_message: str = "ERROR"):
    return JsonResponse({"status": ERROR, "data": None, "error": error_message})


def get_method_error(req, supported_method):
    return JsonResponse(
        {
            "status": ERROR,
            "data": None,
            "error": f"{req.method} method is not supported. SUPPORTED METHODS: [{supported_method}]",
        }
    )


# TODO has to modify token exp in DAYS && time=30.
def create_token(payload, time=180):
    payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(seconds=time)
    return encode(payload, settings.SECRET_KEY, algorithm="HS256")


# TODO token exp to be modified in terms of minutes after dev.
def generate_tokens(user: User, access_token_exp=180, refresh_token_exp=300):
    payload = {"id": str(user.id), "username": user.username}
    token, refresh_token = create_token(payload, access_token_exp), create_token(
        payload, refresh_token_exp
    )
    return {
        "id": str(user.id),
        "access_token": token,
        "refresh_token": refresh_token,
    }
