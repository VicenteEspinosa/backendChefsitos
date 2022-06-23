import json

from django.http import JsonResponse

from recipelib.infrastructure.validation.formats import email
from recipelib.models import User
from recipelib.serializers import UserSerializer


def show(request):
    try:
        return JsonResponse(
            UserSerializer(request.user).data, safe=False, status=200
        )
    except Exception as error:
        print(error)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": str(error),
            },
            safe=False,
            status=500,
        )


def show_by_id(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse(
            UserSerializer(user, context={"request": request}).data,
            safe=False,
            status=200,
        )
    except Exception as error:
        print(error)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": str(error),
            },
            safe=False,
            status=500,
        )
