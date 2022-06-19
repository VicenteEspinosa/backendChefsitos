from django.http import JsonResponse

from recipelib.utils import error_json_response


def unfollow(req, user):
    try:
        req.user.profile.following.remove(user.profile)
        req.user.save()
        return JsonResponse(
            {"message": "User unfollowed successfully"},
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)
