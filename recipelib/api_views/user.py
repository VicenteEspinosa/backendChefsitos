from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from recipelib.operations.users.signup import signup
from recipelib.operations.users.signin import signin
from recipelib.operations.users.signout import signout


@method_decorator(csrf_exempt, name='dispatch')
class UserSignup(View):
    def post(self, request):
        return signup(request)

@method_decorator(csrf_exempt, name='dispatch')
class UserSignin(View):
    def post(self, request):
        return signin(request)

@method_decorator(csrf_exempt, name='dispatch')
class UserSignout(View):
    def post(self, request):
        return signout(request)