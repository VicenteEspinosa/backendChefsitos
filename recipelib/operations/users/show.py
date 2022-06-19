import json

from django.http import JsonResponse

from recipelib.infrastructure.validation.formats import email
from recipelib.models import User
from recipelib.serializers import UserSerializer


def show(request):
    try:
        return JsonResponse(
            UserSerializer(request.user).data, safe=False, status=201
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


def show_by_id(_, user_id):
    try:
        user = User.objects.get(pk=user_id)
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
