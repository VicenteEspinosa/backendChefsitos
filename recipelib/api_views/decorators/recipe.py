from functools import wraps

from recipelib.models import Recipe
from recipelib.utils import (
    error_json_response,
    not_found_json_response,
    not_owner_json_response,
)


def find_recipe_by_id(view):
    @wraps(view)
    def wrapper(request, recipe_id, *args, **kwargs):
        try:
            recipe_array = Recipe.objects.filter(pk=recipe_id)
            if recipe_array:
                return view(request, recipe_array[0], *args, **kwargs)
            return not_found_json_response("recipe")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper


def recipe_belongs_to_user(view):
    @wraps(view)
    def wrapper(request, recipe, *args, **kwargs):
        try:
            if request.user.is_superuser or request.user.id == recipe.user.id:
                return view(request, recipe, *args, **kwargs)
            return not_owner_json_response()
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper
