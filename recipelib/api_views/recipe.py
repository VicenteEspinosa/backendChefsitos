from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from recipelib.api_views.decorators.recipe import find_recipe_by_id
from recipelib.api_views.decorators.user import logged_in_check
from recipelib.infrastructure.validation.request_validation import (
    validate_request,
)
from recipelib.operations.recipes.recipe_actions import (
    create_recipe,
    get_self_recipes,
    get_single_recipe,
)


@method_decorator(csrf_exempt, name="dispatch")
class RecipeView(View):
    @method_decorator(logged_in_check)
    def post(self, req):
        return validate_request(req, create_recipe)


@method_decorator(csrf_exempt, name="dispatch")
class SelfRecipesView(View):
    @method_decorator(logged_in_check)
    def get(self, req):
        return get_self_recipes(req)


@method_decorator(csrf_exempt, name="dispatch")
class SingleRecipeView(View):
    @method_decorator(logged_in_check)
    @method_decorator(find_recipe_by_id)
    def get(self, req, recipe):
        return get_single_recipe(req, recipe)
