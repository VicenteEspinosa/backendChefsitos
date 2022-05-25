import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import Tag, User


class TestTagViews(TransactionTestCase):
    reset_sequences = True

    # DELETE #
    def test_tag_DELETE_by_id_when_item_exists(self):
        Tag.objects.create(name="pastas", placeholder_url="test")
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("tags", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.count(), initial_total - 1)

    def test_tag_DELETE_by_id_when_item_does_not_exist(self):
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("tags", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tag.objects.count(), initial_total)

    def test_tag_DELETE_not_admin(self):
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="normal_user_test")[0]
        )
        url = reverse("tags", args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tag.objects.count(), initial_total)

    def test_tag_DELETE_not_logged_in(self):
        initial_total = Tag.objects.count()
        url = reverse("tags", args=[1])
        response = Client().delete(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Tag.objects.count(), initial_total)

    # GET #
    def test_tag_GET_all(self):
        url = reverse("tags")
        response = Client().get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_tag_GET_by_id_when_item_exists(self):
        Tag.objects.create(name="pastas", placeholder_url="test")
        url = reverse("tags", args=[1])
        response = Client().get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(data.get("name"), "pastas")

    def test_tag_GET_by_id_when_item_does_not_exist(self):
        url = reverse("tags", args=[1])
        response = Client().get(url)
        self.assertEqual(response.status_code, 404)

    # POST #
    def test_tag_POST(self):
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("tags")
        body = {"name": "pastas", "placeholder_url": "test"}
        response = client.post(url, body, content_type="application/json")
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("name"), "pastas")
        self.assertEqual(Tag.objects.count(), initial_total + 1)

    def test_tag_POST_already_exists(self):
        Tag.objects.create(name="pastas")
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("tags")
        body = {"name": "pastas", "placeholder_url": "test"}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(Tag.objects.count(), initial_total)

    def test_tag_POST_bad_request(self):
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(
                username="admin_test", is_superuser=True
            )[0]
        )
        url = reverse("tags")
        body = {}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Tag.objects.count(), initial_total)

    def test_tag_POST_not_admin(self):
        initial_total = Tag.objects.count()
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="normal_user_test")[0]
        )
        url = reverse("tags")
        body = {"name": "pastas", "placeholder_url": "test"}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tag.objects.count(), initial_total)

    def test_tag_POST_not_logged_in(self):
        initial_total = Tag.objects.count()
        url = reverse("tags")
        body = {"name": "pastas", "placeholder_url": "test"}
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Tag.objects.count(), initial_total)
