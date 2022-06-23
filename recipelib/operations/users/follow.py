from django.http import JsonResponse

from recipelib.serializers import FollowingSerializer
from recipelib.utils import error_json_response


def follow(req, user):
    try:
        req.user.profile.following.add(user.profile)
        req.user.save()
        return JsonResponse(
            FollowingSerializer(req.user).data,
            safe=False,
            status=201,
        )

    except Exception as err:
        print(err)
        return error_json_response(err)
