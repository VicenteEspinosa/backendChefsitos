from functools import wraps

from recipelib.models import Ingredient
from recipelib.utils import error_json_response, not_found_json_response


def find_ingredient_by_id(view):
    @wraps(view)
    def wrapper(request, ingredient_id, *args, **kwargs):
        try:
            ingredient_array = Ingredient.objects.filter(pk=ingredient_id)
            if ingredient_array:
                return view(request, ingredient_array[0], *args, **kwargs)
            return not_found_json_response("ingredient")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper
