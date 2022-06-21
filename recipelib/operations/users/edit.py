import json

from django.http import JsonResponse

from recipelib.infrastructure.validation.formats import email
from recipelib.models import User
from recipelib.serializers import UserSerializer
from recipelib.utils import already_exists_json_response, internal_error

schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "email": {"pattern": email, "type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "description": {"type": "string"},
        "picture_url": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": [],
}


def edit(request, data):
    try:
        any = User.objects.filter(username=data.get("username"))
        if not any:
            old_username = request.user.username
            user = User.objects.filter(username=old_username)[0]
            if data.get("username"):
                user.username = data.get("username")
            if data.get("email"):
                user.email = data.get("email")
            if data.get("first_name"):
                user.first_name = data.get("first_name")
            if data.get("last_name"):
                user.last_name = data.get("last_name")
            if data.get("description"):
                user.profile.description = data.get("description")
            if data.get("picture_url"):
                user.profile.picture_url = data.get("picture_url")
            if data.get("password"):
                user.set_password(data.get("password"))
            user.save()
            return JsonResponse(
                UserSerializer(user).data, safe=False, status=200
            )
        return already_exists_json_response(
            "User", "Username", data.get("username")
        )
    except Exception as err:
        print(err)
        return internal_error


edit.schema = schema
