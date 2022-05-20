import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import Measurement, User


class TestMeasurementViews(TransactionTestCase):
    reset_sequences = True

    # DELETE #
    def test_measurement_DELETE_by_id_when_item_exists(self):
        Measurement.objects.create(name="kg")
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("measurements", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Measurement.objects.count(), initial_total - 1)

    def test_measurement_DELETE_by_id_when_item_does_not_exist(self):
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("measurements", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Measurement.objects.count(), initial_total)

    def test_measurement_DELETE_not_admin(self):
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="normal_user_test")[0]
        )
        url = reverse("measurements", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Measurement.objects.count(), initial_total)

    def test_measurement_DELETE_not_logged_in(self):
        initial_total = Measurement.objects.count()
        url = reverse("measurements", args=[1])
        response = Client().delete(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Measurement.objects.count(), initial_total)

    # GET #
    def test_measurement_GET_all(self):
        url = reverse("measurements")
        response = Client().get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_measurement_GET_by_id_when_item_exists(self):
        Measurement.objects.create(name="kg")
        url = reverse("measurements", args=[1])
        response = Client().get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(data.get("name"), "kg")

    def test_measurement_GET_by_id_when_item_does_not_exist(self):
        url = reverse("measurements", args=[1])
        response = Client().get(url)
        self.assertEqual(response.status_code, 404)

    # POST #
    def test_measurement_POST(self):
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("measurements")
        body = {"name": "ml"}
        response = client.post(url, body, content_type="application/json")
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("name"), "ml")
        self.assertEqual(Measurement.objects.count(), initial_total + 1)

    def test_measurement_POST_already_exists(self):
        Measurement.objects.create(name="kg")
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("measurements")
        body = {"name": "kg"}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(Measurement.objects.count(), initial_total)

    def test_measurement_POST_bad_request(self):
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("measurements")
        body = {}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Measurement.objects.count(), initial_total)

    def test_measurement_POST_not_admin(self):
        initial_total = Measurement.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="normal_user_test")[0]
        )
        url = reverse("measurements")
        body = {"name": "ml"}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Measurement.objects.count(), initial_total)

    def test_measurement_POST_not_logged_in(self):
        initial_total = Measurement.objects.count()
        url = reverse("measurements")
        body = {"name": "ml"}
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Measurement.objects.count(), initial_total)
