from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipelib.models import (
    Ingredient,
    Item,
    Measurement,
    Profile,
    Rating,
    Recipe,
    RecipeMeasurementIngredient,
    Tag,
    User,
)


class FollowingSerializer(ModelSerializer):
    following = serializers.SerializerMethodField("get_following")

    class Meta:
        model = User
        fields = (
            "id",
            "following",
        )

    def get_following(self, obj):
        return list(obj.profile.following.all().values_list("user", flat=True))


class UserSerializer(ModelSerializer):
    picture_url = serializers.SerializerMethodField("get_picture_url")
    description = serializers.SerializerMethodField("get_description")
    followers = serializers.SerializerMethodField("get_followers")
    following = serializers.SerializerMethodField("get_following")
    is_following = serializers.SerializerMethodField("get_is_following")

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
            "followers",
            "following",
            "is_following",
            "is_superuser",
        )

    def get_picture_url(self, obj):
        return ProfileSerializer(obj.profile).data.get("picture_url")

    def get_description(self, obj):
        return ProfileSerializer(obj.profile).data.get("description")

    def get_followers(self, obj):
        return list(obj.profile.followers.all().values_list("user", flat=True))

    def get_following(self, obj):
        return list(obj.profile.following.all().values_list("user", flat=True))

    def get_is_following(self, obj):
        if not self.context.get("request", None):
            return None
        current_user = self.context.get("request").user
        if current_user.is_authenticated:
            if current_user.id == obj.id:
                return None
            return (
                obj.profile.followers.all()
                .values_list("user", flat=True)
                .filter(user=current_user)
                .exists()
            )
        return None


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("description", "picture_url", "following")


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


class RecipeTagSerializer(ModelSerializer):
    tag_id = serializers.ReadOnlyField(source="tag.id")
    tag_name = serializers.ReadOnlyField(source="tag.name")
    tag_placeholder_url = serializers.ReadOnlyField(
        source="tag.placeholder_url"
    )

    class Meta:
        model = RecipeMeasurementIngredient

        fields = (
            "id",
            "tag_id",
            "tag_name",
            "tag_placeholder_url",
        )


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "url", "body", "order_number")


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ("recipe_id", "user_id", "like")


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeMeasurementIngredientSerializer(
        source="recipemeasurementingredient_set", many=True, read_only=True
    )
    items = ItemSerializer(source="item_set", many=True, read_only=True)
    tags = RecipeTagSerializer(
        source="recipetag_set", many=True, read_only=True
    )
    ratings = RatingSerializer(source="rating_set", many=True, read_only=True)

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
            "items",
            "tags",
            "user_id",
            "ratings",
        )


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "placeholder_url")
