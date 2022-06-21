import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import (
    Ingredient,
    Measurement,
    Rating,
    Recipe,
    RecipeMeasurementIngredient,
    Tag,
    User,
)
from recipelib.serializers import RecipeSerializer


class TestRecipeViews(TransactionTestCase):
    reset_sequences = True

    # POST #
    def test_recipe_POST(self):
        initial_total = Recipe.objects.count()
        Ingredient.objects.create(name="cebolla")
        Tag.objects.create(name="cebolla", placeholder_url="test")
        Measurement.objects.create(name="un")  # Unidad
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("recipes")
        body = {
            "name": "cebolla picada",
            "description": "",
            "private": False,
            "picture_url": "",
            "items": [{"body": "cortar cebolla en cubos", "order_number": 0}],
            "tagIds": [1],
            "ingredients": [
                {"measurement_id": 1, "ingredient_id": 1, "quantity": 1}
            ],
        }
        response = client.post(url, body, content_type="application/json")
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("name"), "cebolla picada")
        self.assertEqual(Recipe.objects.count(), initial_total + 1)

    def test_recipe_POST_bad_request(self):
        initial_total = Recipe.objects.count()
        Ingredient.objects.create(name="cebolla")
        Tag.objects.create(name="cebolla", placeholder_url="test")
        Measurement.objects.create(name="un")  # Unidad
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("recipes")
        # body without recipe name
        body = {
            "description": "",
            "private": False,
            "picture_url": "",
            "items": [{"body": "cortar cebolla en cubos", "order_number": 0}],
            "tagIds": [],
            "ingredients": [
                {"measurement_id": 1, "ingredient_id": 1, "quantity": 1}
            ],
        }
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Recipe.objects.count(), initial_total)

    def test_recipe_POST_not_logged_in(self):
        initial_total = Recipe.objects.count()
        url = reverse("recipes")
        Ingredient.objects.create(name="cebolla")
        Tag.objects.create(name="cebolla", placeholder_url="test")
        Measurement.objects.create(name="un")  # Unidad
        body = {
            "name": "cebolla picada",
            "description": "",
            "private": False,
            "picture_url": "",
            "items": [{"body": "cortar cebolla en cubos", "order_number": 0}],
            "tagIds": [],
            "ingredients": [
                {"measurement_id": 1, "ingredient_id": 1, "quantity": 1}
            ],
        }
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Recipe.objects.count(), initial_total)

    def test_rate_recipe_when_recipe_exists(self):
        client = Client()
        user = User.objects.get_or_create(username="generic_user")[0]
        client.force_login(user)
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("rate", args=[recipe.id])
        body = {"like": True}
        response = client.post(url, body, content_type="application/json")
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("recipe_id"), recipe.id)
        self.assertEqual(data.get("like"), body["like"])
        self.assertEqual(data.get("user_id"), user.id)

    def test_rate_recipe_when_recipe_not_exists(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("rate", args=[1])
        body = {"like": True}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    # GET #
    def test_GET_all_self_recipes(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("self_recipes")
        response = client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_GET_all_self_recipes_not_logged_in(self):
        url = reverse("self_recipes")
        response = Client().get(url)
        self.assertEqual(response.status_code, 401)

    def test_GET_recipe_by_id_when_item_exists(self):
        ingredient = Ingredient.objects.create(name="cebolla")
        measu = Measurement.objects.create(name="un")  # Unidad
        Tag.objects.create(name="cebolla", placeholder_url="test")

        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        RecipeMeasurementIngredient.objects.create(
            recipe=recipe, measurement=measu, ingredient=ingredient, quantity=1
        )

        url = reverse("recipes", args=[1])
        response = client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(data.get("name"), "cebolla picada")

    def test_GET_recipe_by_id_when_item_does_not_exist(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("recipes", args=[1])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_GET_feed(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("feed")
        response = client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_GET_feed_following(self):
        client = Client()
        current_user = User.objects.get_or_create(username="generic_user")[0]
        client.force_login(current_user)
        followed_user = User.objects.get_or_create(
            username="other_generic_user"
        )[0]
        current_user.profile.following.add(followed_user.profile)
        not_followed_user = User.objects.get_or_create(
            username="another_generic_user"
        )[0]
        recipe_user_followed = Recipe.objects.create(
            user=followed_user,
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        recipe_user_not_followed = Recipe.objects.create(
            user=not_followed_user,
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("following_feed")
        response = client.get(url)
        data = response.json()
        self.assertEqual(
            RecipeSerializer(recipe_user_followed).data in data, True
        )
        self.assertEqual(
            RecipeSerializer(recipe_user_not_followed).data in data, False
        )

    def test_GET_feed_other_users_recipe_is_included(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("feed")
        response = client.get(url)
        data = response.json()
        self.assertEqual(RecipeSerializer(recipe).data in data, True)

    def test_GET_feed_req_users_recipe_is_not_included(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("feed")
        response = client.get(url)
        data = response.json()
        self.assertEqual(RecipeSerializer(recipe).data in data, False)

    def test_GET_feed_is_ordered_by_created_at(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        first_recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        second_recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("feed")
        response = client.get(url)
        data = response.json()
        self.assertEqual(RecipeSerializer(second_recipe).data, data[0])
        self.assertEqual(RecipeSerializer(first_recipe).data, data[1])

    def test_GET_feed_is_ordered_by_popularity(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        first_recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        second_recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        Rating.objects.create(
            user=User.objects.get_or_create(username="generic_user")[0],
            recipe=first_recipe,
            like=True,
        )
        url = reverse("feed")
        response = client.get(url, {"order_by": "popularity"})
        data = response.json()
        self.assertEqual(RecipeSerializer(second_recipe).data, data[1])
        self.assertEqual(RecipeSerializer(first_recipe).data, data[0])

    # DELETE #
    def test_recipe_rating_DELETE_when_rating_exists(self):
        client = Client()
        user = User.objects.get_or_create(username="generic_user")[0]
        client.force_login(user)
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        Rating.objects.create(user=user, recipe=recipe, like=True)
        url = reverse("rate", args=[recipe.id])
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_rating_DELETE_when_rating_not_exists(self):
        client = Client()
        user = User.objects.get_or_create(username="generic_user")[0]
        client.force_login(user)
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_generic_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("rate", args=[recipe.id])
        response = client.delete(url)
        data = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"), "rating not found")

    def test_recipe_DELETE(self):
        current_user = User.objects.get_or_create(username="generic_user")[0]
        client = Client()
        client.force_login(current_user)
        recipe = Recipe.objects.create(
            user=current_user,
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        initial_count = Recipe.objects.count()
        url = reverse("recipes", args=[recipe.id])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipe.objects.count(), initial_count - 1)

    def test_recipe_DELETE_when_recipe_not_found(self):
        current_user = User.objects.get_or_create(username="generic_user")[0]
        client = Client()
        client.force_login(current_user)
        initial_count = Recipe.objects.count()
        url = reverse("recipes", args=[99])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Recipe.objects.count(), initial_count)

    def test_recipe_DELETE_when_user_is_not_owner(self):
        current_user = User.objects.get_or_create(username="generic_user")[0]
        client = Client()
        client.force_login(current_user)
        recipe = Recipe.objects.create(
            user=User.objects.get_or_create(username="other_user")[0],
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        initial_count = Recipe.objects.count()
        url = reverse("recipes", args=[recipe.id])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Recipe.objects.count(), initial_count)

    # PUT #
    def test_recipe_PUT(self):
        Tag.objects.create(name="cebolla", placeholder_url="test")
        Measurement.objects.create(name="gr")
        Ingredient.objects.create(name="cebolla")
        current_user = User.objects.get_or_create(username="generic_user")[0]
        client = Client()
        client.force_login(current_user)
        recipe = Recipe.objects.create(
            user=current_user,
            name="cebolla picada",
            description="",
            private=False,
            picture_url="",
        )
        url = reverse("recipes", args=[recipe.id])
        body = {
            "name": "aji picado",
            "description": "",
            "private": False,
            "picture_url": "",
            "items": [{"body": "cortar cebolla en cubos", "order_number": 0}],
            "tagIds": [1],
            "ingredients": [
                {"measurement_id": 1, "ingredient_id": 1, "quantity": 1}
            ],
        }
        response = client.put(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Recipe.objects.filter(pk=recipe.id)[0].name, "aji picado"
        )

    def test_recipe_PUT_does_not_exist(self):
        current_user = User.objects.get_or_create(username="generic_user")[0]
        client = Client()
        client.force_login(current_user)
        url = reverse("recipes", args=[99])
        body = {
            "name": "aji picado",
        }
        response = client.put(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 404)
