from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from recipelib.api_views.decorators.recipe import (
    find_recipe_by_id,
    recipe_belongs_to_user,
)
from recipelib.api_views.decorators.user import logged_in_check
from recipelib.infrastructure.validation.request_validation import (
    validate_request,
)
from recipelib.operations.recipes.rating_actions import (
    delete_rating,
    rate_recipe,
)
from recipelib.operations.recipes.recipe_actions import (
    create_recipe,
    delete_recipe,
    edit_recipe,
    get_chef_recipes,
    get_feed,
    get_self_recipes,
    get_single_recipe,
)


@method_decorator(csrf_exempt, name="dispatch")
class RecipeView(View):
    @method_decorator(logged_in_check)
    @method_decorator(find_recipe_by_id)
    def get(self, req, recipe):
        return get_single_recipe(req, recipe)

    @method_decorator(logged_in_check)
    def post(self, req):
        return validate_request(req, create_recipe)

    @method_decorator(logged_in_check)
    @method_decorator(find_recipe_by_id)
    @method_decorator(recipe_belongs_to_user)
    def put(self, req, recipe):
        return validate_request(req, edit_recipe, recipe)

    @method_decorator(logged_in_check)
    @method_decorator(find_recipe_by_id)
    @method_decorator(recipe_belongs_to_user)
    def delete(self, req, recipe):
        return delete_recipe(req, recipe)


@method_decorator(csrf_exempt, name="dispatch")
class SelfRecipesView(View):
    @method_decorator(logged_in_check)
    def get(self, req):
        return get_self_recipes(req)


@method_decorator(csrf_exempt, name="dispatch")
class FeedView(View):
    @method_decorator(logged_in_check)
    def get(self, req):
        return get_feed(req)


@method_decorator(csrf_exempt, name="dispatch")
class FollowingFeedView(View):
    @method_decorator(logged_in_check)
    def get(self, req):
        return get_feed(req, following=True)


@method_decorator(csrf_exempt, name="dispatch")
class RateRecipeView(View):
    @method_decorator(logged_in_check)
    @method_decorator(find_recipe_by_id)
    def post(self, req, recipe):
        return validate_request(req, rate_recipe, recipe)

    @method_decorator(logged_in_check)
    @method_decorator(find_recipe_by_id)
    def delete(self, req, recipe):
        return delete_rating(req, recipe)


@method_decorator(csrf_exempt, name="dispatch")
class SocialRecipesView(View):
    @method_decorator(logged_in_check)
    def get(self, req, user_id=None):
        if user_id is not None:
            return get_chef_recipes(req, user_id)
