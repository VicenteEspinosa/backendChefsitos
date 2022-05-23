from django.db import transaction
from django.http import JsonResponse

from recipelib.models import Item, Recipe
from recipelib.serializers import ItemSerializer, RecipeSerializer
from recipelib.utils import error_json_response

schema = {
    "definitions": {
        "Item": {
            "properties": {
                "url": {"type": "string"},
                "body": {"type": "string"},
                "order_number": {"type": "integer"},
            },
            "anyOf": [
                {"required": ["url", "order_number"]},
                {"required": ["body", "order_number"]},
            ],
        },
    },
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "picture_url": {"type": "string"},
        "private": {"type": "boolean"},
        "items": {
            "type": "array",
            "items": {"$ref": "#/definitions/Item"},
        },
    },
    "required": ["name", "items"],
}


def create_recipe(req, data):
    try:
        with transaction.atomic():
            items = data["items"]
            del data["items"]
            recipe = Recipe.objects.create(**data, user=req.user)
            recipe.save()
            items = Item.objects.bulk_create(
                [Item(**item, recipe=recipe) for item in items]
            )
            return JsonResponse(
                {
                    **RecipeSerializer(recipe).data,
                    "items": [ItemSerializer(item).data for item in items],
                },
                safe=False,
                status=201,
            )
    except Exception as err:
        print(err)
        return error_json_response(err)


create_recipe.schema = schema
