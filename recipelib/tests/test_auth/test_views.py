import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import User


class TestAuthViews(TransactionTestCase):
    reset_sequences = True

    # POST #
    def test_signin(self):
        client = Client()
        new_user = User.objects.create(
            username="myuser",
            email="email@email.com",
            first_name="first",
            last_name="last",
        )
        new_user.set_password("myuserpassword")
        new_user.save()
        url = reverse("user_signin")
        body = {"username": "myuser", "password": "myuserpassword"}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_signin_wrong_credentials(self):
        client = Client()
        new_user = User.objects.create(
            username="myuser",
            email="email@email.com",
            first_name="first",
            last_name="last",
        )
        new_user.set_password("anotherpassword")
        new_user.save()
        url = reverse("user_signin")
        body = {"username": "myuser", "password": "myuserpassword"}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_signout(self):
        client = Client()
        client.force_login(
            User.objects.get_or_create(username="normal_user_test")[0]
        )
        url = reverse("user_signout")
        body = {}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        user_count = User.objects.count()
        url = reverse("user_signup")
        body = {
            "username": "testeo",
            "email": "test@uc.cl",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "password": "clave",
        }
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_signup_user_already_exists(self):
        new_user = User.objects.create(
            username="testeo",
            email="email@email.com",
            first_name="first",
            last_name="last",
        )
        new_user.set_password("myuserpassword")
        new_user.save()
        user_count = User.objects.count()
        url = reverse("user_signup")
        body = {
            "username": "testeo",
            "email": "test@uc.cl",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "password": "clave",
        }
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(User.objects.count(), user_count)
