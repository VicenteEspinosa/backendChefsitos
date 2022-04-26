import json
from recipelib.models import User
from django.http import JsonResponse
from recipelib.serializers import UserSerializer

def singup(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        user = User.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
        )
        user.set_password(data.get('password'))
        user.save()

        return JsonResponse(UserSerializer(user).data, safe=False, status=201)
    except Exception as err:
        print(err)
    return JsonResponse({"message": "Error"}, safe=False, status=400)