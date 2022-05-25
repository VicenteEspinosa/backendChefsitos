import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import (
    Ingredient,
    Measurement,
    Recipe,
    RecipeMeasurementIngredient,
    Tag,
    User,
)


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
        self.assertEqual(response.status_code, 500)
