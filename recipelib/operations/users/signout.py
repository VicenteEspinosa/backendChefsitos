from django.contrib.auth import logout
from django.http import JsonResponse


def signout(request):
    try:
        logout(request)
        return JsonResponse({}, safe=False, status=200)
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
