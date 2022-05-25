from functools import wraps

from recipelib.models import Tag
from recipelib.utils import error_json_response, not_found_json_response


def find_tag_by_id(view):
    @wraps(view)
    def wrapper(request, tag_id, *args, **kwargs):
        try:
            tag_array = Tag.objects.filter(pk=tag_id)
            if tag_array:
                return view(request, tag_array[0], *args, **kwargs)
            return not_found_json_response("tag")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper
