from functools import wraps

from recipelib.models import Recipe
from recipelib.utils import error_json_response, not_found_json_response


def find_recipe_by_id(view):
    @wraps(view)
    def wrapper(request, recipe_id, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe:
                return view(request, recipe, *args, **kwargs)
            return not_found_json_response("recipe")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper
