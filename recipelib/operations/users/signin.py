import json
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from recipelib.serializers import UserSerializer

def signin(request):
  try:
    data = json.loads(request.body.decode('utf-8'))
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    if user is not None:
      login(request, user)
      return JsonResponse(UserSerializer(user).data, safe=False, status=201)
    else:
      return JsonResponse(safe=False, status=404)
  except Exception as err:
    print(err)
  return JsonResponse({"message": "Error"}, safe=False, status=400)
    