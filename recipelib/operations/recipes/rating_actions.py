from django.http import JsonResponse

from recipelib.models import Rating
from recipelib.serializers import RatingSerializer
from recipelib.utils import error_json_response, not_found_json_response


def rate_recipe(req, data, recipe):
    try:
        rating = Rating.objects.get_or_create(recipe=recipe, user=req.user)[0]
        rating.like = data["like"]
        rating.save()
        return JsonResponse(
            RatingSerializer(rating).data,
            safe=False,
            status=201,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


rate_recipe.schema = {
    "type": "object",
    "properties": {
        "like": {"type": "boolean"},
    },
    "required": ["like"],
}


def delete_rating(req, recipe):
    try:
        rating = Rating.objects.filter(recipe=recipe, user=req.user)
        if rating:
            rating[0].delete()
            return JsonResponse(
                {"message": "Rating deleted successfully"},
                safe=False,
                status=200,
            )
        else:
            return not_found_json_response("rating")
    except Exception as err:
        print(err)
        return error_json_response(err)
