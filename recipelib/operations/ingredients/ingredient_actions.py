from django.http import JsonResponse

from recipelib.models import Ingredient
from recipelib.serializers import IngredientSerializer
from recipelib.utils import (
    already_exists_json_response,
    empty_string_json_response,
    error_json_response,
)

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
    },
    "required": ["name"],
}


def create_ingredient(req, data):
    try:
        lowercase_name = str(data.get("name")).lower()
        if not len(lowercase_name):
            return empty_string_json_response("name")
        ingredient = Ingredient.objects.filter(name=lowercase_name)
        if ingredient:
            return already_exists_json_response(
                "ingredient", "name", ingredient[0].name
            )
        ingredient = Ingredient.objects.create(name=lowercase_name)
        ingredient.save()
        return JsonResponse(
            IngredientSerializer(ingredient).data, safe=False, status=201
        )

    except Exception as err:
        print(err)
        return error_json_response(err)


create_ingredient.schema = schema


def get_all_ingredients(req):
    try:
        ingredients = Ingredient.objects.all()
        return JsonResponse(
            IngredientSerializer(ingredients, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def get_ingredient(req, ingredient):
    try:
        return JsonResponse(
            IngredientSerializer(ingredient).data, safe=False, status=200
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def delete_ingredient(req, ingredient):
    try:
        ingredient.delete()
        return JsonResponse(
            {"message": "ingredient deleted successfully"},
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)
