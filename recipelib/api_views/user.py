from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from recipelib.operations.users.singup import singup


@method_decorator(csrf_exempt, name='dispatch')
class UserSignup(View):
    def post(self, request):
        return singup(request)
