from django.contrib.auth import logout
from django.http import JsonResponse

def signout(request):
  try:
    logout(request)
    return JsonResponse({}, safe=False, status=201)
  except Exception as err:
    print(err)
  return JsonResponse({"message": "Error"}, safe=False, status=400)
  