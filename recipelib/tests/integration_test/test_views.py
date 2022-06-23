import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import Measurement, User
from recipelib.tests.integration_test.testing_data import test_user


class IntegrationTest(TransactionTestCase):
    reset_sequences = True

    def test_create_recipe_full_path(self):
        # user signup
        client = Client()
        url = reverse("user_signup")
        response = client.post(url, test_user, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # user signin
        url = reverse("user_signin")
        body = {
            "username": test_user["username"],
            "password": test_user["password"],
        }
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # not tesint measurement creation
        Measurement.objects.create(name="unidadmultivalente")  # Unidad

        # create ingredients
        url = reverse("ingredients")
        body = {"name": "pan"}
        response = client.post(url, body, content_type="application/json")
        ing_pan_data = response.json()
        self.assertEqual(response.status_code, 201)
        body = {"name": "mermelada"}
        response = client.post(url, body, content_type="application/json")
        ing_mer_data = response.json()
        self.assertEqual(response.status_code, 201)

        # create recipe
        url = reverse("recipes")
        body = {
            "name": "Pan con mermelada",
            "description": "Simple y efectivo, para el desayuno",
            "private": False,
            "picture_url": "",
            "items": [{"body": "untar mermelada en pan", "order_number": 0}],
            "tagIds": [],
            "ingredients": [
                {
                    "measurement_id": 1,
                    "ingredient_id": ing_pan_data["id"],
                    "quantity": 2,
                },
                {
                    "measurement_id": 1,
                    "ingredient_id": ing_mer_data["id"],
                    "quantity": 1,
                },
            ],
        }
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 201)
