import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from recipelib.serializers import UserSerializer

schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
}


def signin(req, data):
    try:
        user = authenticate(
            req, username=data.get("username"), password=data.get("password")
        )
        if user is not None:
            login(req, user)
            return JsonResponse(
                UserSerializer(user).data, safe=False, status=200
            )
        else:
            return JsonResponse(
                {
                    "internalCode": "entity-not-found",
                    "message": "wrong credentials",
                },
                safe=False,
                status=401,
            )
    except Exception as err:
        print(err)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": "An error has ocurred",
            },
            safe=False,
            status=500,
        )


signin.schema = schema
