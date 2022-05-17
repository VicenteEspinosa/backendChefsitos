import json

from django.http import JsonResponse

from recipelib.infrastructure.validation.formats import email
from recipelib.models import User
from recipelib.serializers import UserSerializer

schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"pattern": email, "type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "email", "first_name", "last_name", "password"],
}


def signup(req, data):
    try:
        user = User.objects.filter(username=data.get("username"))
        if user:
            return JsonResponse(
                {
                    "internalCode": "entity-not-processable",
                    "path": "username",
                    "message": "'username' is already signed up",
                },
                safe=False,
                status=422,
            )
        user = User.objects.create(
            username=data.get("username"),
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
        )
        user.set_password(data.get("password"))
        user.save()

        return JsonResponse(UserSerializer(user).data, safe=False, status=201)
    except Exception as err:
        print(err)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": "An error has ocurred",
                "message": "An error has ocurred",
            },
            safe=False,
            status=500,
        )


signup.schema = schema
