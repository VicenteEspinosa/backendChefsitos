from functools import wraps

from recipelib.models import Measurement
from recipelib.utils import (
    not_an_admin_json_response,
    not_logged_in_json_response,
)


def logged_in_check(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_logged_in_json_response()
        return view(request, *args, **kwargs)

    return wrapper


def admin_check(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return not_logged_in_json_response()
        if not request.user.is_superuser:
            return not_an_admin_json_response()
        return view(request, *args, **kwargs)

    return wrapper
