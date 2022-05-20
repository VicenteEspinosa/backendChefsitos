from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from recipelib.api_views.decorators.ingredient import (
    find_ingredient_by_id,
)
from recipelib.api_views.decorators.user import (
    admin_check,
    logged_in_check,
)
from recipelib.infrastructure.validation.request_validation import (
    validate_request,
)
from recipelib.operations.ingredients.ingredient_actions import (
    create_ingredient,
    delete_ingredient,
    get_all_ingredients,
    get_ingredient,
)


@method_decorator(csrf_exempt, name="dispatch")
class IngredientView(View):
    def get(self, req, ingredient_id=None):
        if ingredient_id is not None:
            return self.get_specific(req, ingredient_id)
        return get_all_ingredients(req)

    @method_decorator(find_ingredient_by_id)
    def get_specific(self, req, ingredient):
        return get_ingredient(req, ingredient)

    @method_decorator(logged_in_check)
    def post(self, req):
        return validate_request(req, create_ingredient)

    @method_decorator(admin_check)
    @method_decorator(find_ingredient_by_id)
    def delete(self, req, ingredient):
        return delete_ingredient(req, ingredient)
