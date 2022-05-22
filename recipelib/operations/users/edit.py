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
    },
    "required": ["username", "email", "first_name", "last_name"],
}


def edit(request, data):
    try:
        any = User.objects.filter(username=data.get("username"))
        print(any)
        print(data.get("username"))
        if not any:
            old_username = request.user.username
            user = User.objects.filter(username=old_username)[0]
            user.username = data.get("username")
            user.email = data.get("email")
            user.first_name = data.get("first_name")
            user.last_name = data.get("last_name")
            user.save()
            return JsonResponse(
                UserSerializer(user).data, safe=False, status=201
            )
        return JsonResponse(
            {
                "internalCode": "entity-not-processable",
                "path": "username",
                "message": "'username' already exists",
            },
            safe=False,
            status=422,
        )
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


edit.schema = schema
