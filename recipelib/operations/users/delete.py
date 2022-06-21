import json

from django.http import JsonResponse

from recipelib.infrastructure.validation.formats import email
from recipelib.models import User
from recipelib.serializers import UserSerializer


def delete(request):
    try:
        request.user.delete()
        success = {"message": "user deleted successfully"}
        return JsonResponse(success, safe=False, status=200)
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
