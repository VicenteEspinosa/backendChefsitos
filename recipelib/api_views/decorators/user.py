from functools import wraps

from django.contrib.auth.models import User

from recipelib.utils import (
    error_json_response,
    itself_error_json_response,
    not_an_admin_json_response,
    not_found_json_response,
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


def find_user_by_id(view):
    @wraps(view)
    def wrapper(request, user_id, *args, **kwargs):
        try:
            user_array = User.objects.filter(pk=user_id)
            if user_array:
                return view(request, user_array[0], *args, **kwargs)
            return not_found_json_response("user")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper


def not_himself_check(view):
    @wraps(view)
    def wrapper(request, user, *args, **kwargs):
        try:
            if request.user.id == user.id:
                return itself_error_json_response("user")
            return view(request, user, *args, **kwargs)
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper


def requester_is_following(view):
    @wraps(view)
    def wrapper(request, user, *args, **kwargs):
        try:
            check_following_array = (
                request.user.profile.following.all().values_list(
                    "user", flat=True
                )
            )
            if user.id in check_following_array:
                return view(request, user, *args, **kwargs)
            return not_found_json_response("following relationship")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper
