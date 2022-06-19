from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from recipelib.api_views.decorators.user import logged_in_check
from recipelib.infrastructure.validation.request_validation import (
    validate_request,
)
from recipelib.operations.users.delete import delete
from recipelib.operations.users.edit import edit
from recipelib.operations.users.show import show, show_by_id
from recipelib.operations.users.signin import signin
from recipelib.operations.users.signout import signout
from recipelib.operations.users.signup import signup


@method_decorator(csrf_exempt, name="dispatch")
class UserSignup(View):
    def post(self, request):
        return validate_request(request, signup)


@method_decorator(csrf_exempt, name="dispatch")
class UserSignin(View):
    def post(self, request):
        return validate_request(request, signin)


@method_decorator(csrf_exempt, name="dispatch")
class UserSignout(View):
    def post(self, request):
        return signout(request)


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    @method_decorator(logged_in_check)
    def get(self, request):
        return show(request)

    @method_decorator(logged_in_check)
    def post(self, request):
        return validate_request(request, edit)

    @method_decorator(logged_in_check)
    def delete(self, request):
        return delete(request)


class SocialUserView(View):
    def get(self, request, user_id=None):
        if user_id is not None:
            return show_by_id(request, user_id)
