import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import Ingredient, User


class TestIngredientViews(TransactionTestCase):
    reset_sequences = True

    # DELETE #
    def test_ingredient_DELETE_by_id_when_item_exists(self):
        Ingredient.objects.create(name="cebolla")
        initial_total = Ingredient.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("ingredients", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredient.objects.count(), initial_total - 1)

    def test_ingredient_DELETE_by_id_when_item_does_not_exist(self):
        initial_total = Ingredient.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("ingredients", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Ingredient.objects.count(), initial_total)

    def test_ingredient_DELETE_not_admin(self):
        initial_total = Ingredient.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="normal_user_test")[0]
        )
        url = reverse("ingredients", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Ingredient.objects.count(), initial_total)

    def test_ingredient_DELETE_not_logged_in(self):
        initial_total = Ingredient.objects.count()
        url = reverse("ingredients", args=[1])
        response = Client().delete(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Ingredient.objects.count(), initial_total)

    # GET #
    def test_ingredient_GET_all(self):
        url = reverse("ingredients")
        response = Client().get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_ingredient_GET_by_id_when_item_exists(self):
        Ingredient.objects.create(name="cebolla")
        url = reverse("ingredients", args=[1])
        response = Client().get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(data.get("name"), "cebolla")

    def test_ingredient_GET_by_id_when_item_does_not_exist(self):
        url = reverse("ingredients", args=[1])
        response = Client().get(url)
        self.assertEqual(response.status_code, 404)

    # POST #
    def test_ingredient_POST(self):
        initial_total = Ingredient.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("ingredients")
        body = {"name": "cebolla"}
        response = client.post(url, body, content_type="application/json")
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("name"), "cebolla")
        self.assertEqual(Ingredient.objects.count(), initial_total + 1)

    def test_ingredient_POST_already_exists(self):
        Ingredient.objects.create(name="cebolla")
        initial_total = Ingredient.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("ingredients")
        body = {"name": "CeBolLa"}  # Check must be case insensitive
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(Ingredient.objects.count(), initial_total)

    def test_ingredient_POST_bad_request(self):
        initial_total = Ingredient.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="generic_user")[0]
        )
        url = reverse("ingredients")
        body = {}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Ingredient.objects.count(), initial_total)

    def test_ingredient_POST_not_logged_in(self):
        initial_total = Ingredient.objects.count()
        url = reverse("ingredients")
        body = {"name": "cebolla"}
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Ingredient.objects.count(), initial_total)
