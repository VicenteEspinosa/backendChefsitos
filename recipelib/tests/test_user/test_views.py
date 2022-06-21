import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import User


class TestUserViews(TransactionTestCase):
    reset_sequences = True

    # DELETE #
    def test_user_DELETE(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="admin_test")[0]
        )
        initial_total = User.objects.count()
        url = reverse("user_delete")
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), initial_total - 1)

    # GET #
    def test_user_SHOW(self):
        client = Client()
        current_user = User.objects.get_or_create(username="show_test")[0]
        client.force_login(current_user)
        url = reverse("user_view")
        response = client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id", -1), current_user.id)

    def test_user_SHOW_by_id(self):
        client = Client()
        another_user = User.objects.get_or_create(username="another")[0]
        client.force_login(User.objects.get_or_create(username="show_test")[0])
        url = reverse("user_show_by_id", args=[another_user.id])
        response = client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("id", -1), another_user.id)

    # POST #

    def test_user_EDIT(self):
        client = Client()
        current_user = User.objects.get_or_create(username="edit_test")[0]
        current_user.save()
        client.force_login(current_user)
        url = reverse("user_edit")
        body = {
            "username": "editado",
            "email": "test@uc.cl",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "password": "clave",
        }
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.filter(pk=current_user.id)[0].username, "editado"
        )

    def test_user_EDIT_when_new_username_is_taken(self):
        client = Client()
        current_user = User.objects.get_or_create(username="edit_test")[0]
        User.objects.get_or_create(username="taken")[0]
        current_user.save()
        client.force_login(current_user)
        url = reverse("user_edit")
        body = {
            "username": "taken",
            "email": "test@uc.cl",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "password": "clave",
        }
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            User.objects.filter(pk=current_user.id)[0].username, "edit_test"
        )
