from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse

from recipelib.models import (
    Ingredient,
    Item,
    Measurement,
    Recipe,
    RecipeMeasurementIngredient,
    RecipeTag,
    Tag,
)
from recipelib.serializers import RecipeSerializer
from recipelib.utils import error_json_response, not_found_json_response

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
        "Ingredient": {
            "properties": {
                "measurement_id": {"type": "integer"},
                "ingredient_id": {"type": "integer"},
                "quantity": {"type": "integer"},
            },
            "required": ["measurement_id", "ingredient_id", "quantity"],
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
        "tagIds": {
            "type": "array",
            "items": {
                "type": "integer",
            },
            "uniqueItems": True,
        },
        "ingredients": {
            "type": "array",
            "items": {"$ref": "#/definitions/Ingredient"},
        },
    },
}


def create_recipe(req, data):
    try:
        tags = Tag.objects.filter(id__in=data["tagIds"])
        if len(tags) != len(data["tagIds"]):
            tag_ids = [tag.id for tag in tags]
            return not_found_json_response(
                f"tagIds: {[ tag_id for tag_id in data['tagIds'] if tag_id not in tag_ids ]}"
            )
        req_measurement_ids = [
            item["measurement_id"] for item in data["ingredients"]
        ]
        measurements = Measurement.objects.filter(id__in=req_measurement_ids)
        measurement_ids = [measurement.id for measurement in measurements]
        measurement_ids_not_founds = [
            measurement_id
            for measurement_id in req_measurement_ids
            if measurement_id not in measurement_ids
        ]
        if len(measurement_ids_not_founds) != 0:
            return not_found_json_response(
                f"measurementIds: {measurement_ids_not_founds}"
            )
        req_ingredient_ids = [
            item["ingredient_id"] for item in data["ingredients"]
        ]
        ingredients = Ingredient.objects.filter(id__in=req_ingredient_ids)
        ingredient_ids = [ingredient.id for ingredient in ingredients]
        ingredient_ids_not_founds = [
            ingredient_id
            for ingredient_id in req_ingredient_ids
            if ingredient_id not in ingredient_ids
        ]
        if len(ingredient_ids_not_founds) != 0:
            return not_found_json_response(
                f"ingredientIds: {ingredient_ids_not_founds}"
            )
        with transaction.atomic():
            recipe = Recipe.objects.create(
                **{
                    k: data[k]
                    for k in data.keys() - {"items", "tagIds", "ingredients"}
                },
                user=req.user,
            )
            recipe.save()
            Item.objects.bulk_create(
                [Item(**item, recipe=recipe) for item in data["items"]]
            )
            RecipeMeasurementIngredient.objects.bulk_create(
                [
                    RecipeMeasurementIngredient(**item, recipe=recipe)
                    for item in data["ingredients"]
                ]
            )
            RecipeTag.objects.bulk_create(
                [RecipeTag(tag_id=id, recipe=recipe) for id in data["tagIds"]]
            )

            return JsonResponse(
                {
                    **RecipeSerializer(recipe).data,
                },
                safe=False,
                status=201,
            )
    except Exception as err:
        print(err)
        return error_json_response(err)


create_recipe.schema = {
    **schema,
    "required": ["name", "items", "tagIds", "ingredients"],
}


def edit_recipe(req, data, recipe):
    try:
        with transaction.atomic():
            Recipe.objects.filter(pk=recipe.id).update(
                **{
                    k: data[k]
                    for k in data.keys() - {"items", "tagIds", "ingredients"}
                }
            )
            if "items" in data.keys():
                Item.objects.filter(recipe=recipe).delete()
                Item.objects.bulk_create(
                    [Item(**item, recipe=recipe) for item in data["items"]]
                )
            if "tagIds" in data.keys():
                RecipeTag.objects.filter(recipe=recipe).delete()
                RecipeTag.objects.bulk_create(
                    [
                        RecipeTag(tag_id=id, recipe=recipe)
                        for id in data["tagIds"]
                    ]
                )
            if "ingredients" in data.keys():
                RecipeMeasurementIngredient.objects.filter(
                    recipe=recipe
                ).delete()
                RecipeMeasurementIngredient.objects.bulk_create(
                    [
                        RecipeMeasurementIngredient(**item, recipe=recipe)
                        for item in data["ingredients"]
                    ]
                )
            recipe = Recipe.objects.get(pk=recipe.id)

        return JsonResponse(
            RecipeSerializer(recipe).data,
            safe=False,
            status=201,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


edit_recipe.schema = schema


def get_self_recipes(req):
    try:
        recipes = Recipe.objects.filter(user=req.user).order_by("-created_at")
        return JsonResponse(
            RecipeSerializer(recipes, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def get_single_recipe(req, recipe):
    try:
        return JsonResponse(
            RecipeSerializer(recipe).data,
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def delete_recipe(req, recipe):
    try:
        recipe.delete()
        return JsonResponse(
            {"message": "Recipe deleted successfully"},
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def get_feed(req):
    try:
        recipes = Recipe.objects.filter(~Q(user=req.user)).order_by(
            "-created_at"
        )
        return JsonResponse(
            RecipeSerializer(recipes, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)
