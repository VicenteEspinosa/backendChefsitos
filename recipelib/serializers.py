from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipelib.models import (
    Ingredient,
    Item,
    Measurement,
    Profile,
    Recipe,
    RecipeMeasurementIngredient,
    User,
)


class UserSerializer(ModelSerializer):
    picture_url = serializers.SerializerMethodField("get_picture_url")
    description = serializers.SerializerMethodField("get_description")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "description",
            "picture_url",
        )

    def get_picture_url(self, obj):
        return ProfileSerializer(obj.profile).data.get("picture_url")

    def get_description(self, obj):
        return ProfileSerializer(obj.profile).data.get("description")


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("description", "picture_url")


class MeasurementSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "id",
            "name",
        )


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
        )


class RecipeMeasurementIngredientSerializer(ModelSerializer):
    ingredient_id = serializers.ReadOnlyField(source="ingredient.id")
    ingredient_name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_id = serializers.ReadOnlyField(source="measurement.id")
    measurement_name = serializers.ReadOnlyField(source="measurement.name")

    class Meta:
        model = RecipeMeasurementIngredient

        fields = (
            "id",
            "ingredient_id",
            "ingredient_name",
            "measurement_id",
            "measurement_name",
            "quantity",
        )


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeMeasurementIngredientSerializer(
        source="recipemeasurementingredient_set", many=True, read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "picture_url",
            "description",
            "private",
            "created_at",
            "updated_at",
            "ingredients",
        )


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "url", "body", "order_number")
