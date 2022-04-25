from django.views import View
import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
from recipelib.serializers import UserSerializer
from recipelib.models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserSignup(View):
    def post(self, request):
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

            headers = {'content-type': 'application/json'}
            return JsonResponse(UserSerializer(user).data, safe=False, status=201)
        except Exception as err:
            print(err)
        return JsonResponse({"message": "Error"}, safe=False, status=400)
