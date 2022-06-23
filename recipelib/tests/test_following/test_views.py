import json

from django.template.defaultfilters import slugify
from django.test import Client, TransactionTestCase
from django.urls import reverse

from recipelib.models import User


class TestUserFollowViews(TransactionTestCase):
    # DELETE #
    def test_user_follow_DELETE(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        target_user = User.objects.get_or_create(username="target_user")[0]
        current_user.profile.following.add(target_user.profile)
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[target_user.id])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total - 1
        )

    def test_user_follow_DELETE_not_logged_in(self):
        current_user = User.objects.get_or_create(username="current_user")[0]
        target_user = User.objects.get_or_create(username="target_user")[0]
        initial_total = current_user.profile.following.all().count()
        url = reverse("user_follow", args=[target_user.id])
        response = Client().delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )

    def test_user_follow_DELETE_when_requester_is_not_following(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        target_user = User.objects.get_or_create(username="target_user")[0]
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[target_user.id])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )

    def test_user_follow_DELETE_when_target_does_not_exist(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[99])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )

    def test_user_follow_DELETE_when_user_unfollows_itself(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[current_user.id])
        response = client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )

    # POST #
    def test_user_follow_POST(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        target_user = User.objects.get_or_create(username="target_user")[0]
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[target_user.id])
        body = {}
        response = client.post(url, body, content_type="application/json")
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("following")[0], target_user.id)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total + 1
        )

    def test_user_follow_POST_not_logged_in(self):
        current_user = User.objects.get_or_create(username="current_user")[0]
        target_user = User.objects.get_or_create(username="target_user")[0]
        initial_total = current_user.profile.following.all().count()
        url = reverse("user_follow", args=[target_user.id])
        body = {}
        response = Client().post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )

    def test_user_follow_POST_when_target_does_not_exist(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[99])
        body = {}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )

    def test_user_follow_POST_when_user_follows_itself(self):
        client = Client()
        current_user = User.objects.get_or_create(username="current_user")[0]
        initial_total = current_user.profile.following.all().count()
        client.force_login(current_user)
        url = reverse("user_follow", args=[current_user.id])
        body = {}
        response = client.post(url, body, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            current_user.profile.following.all().count(), initial_total
        )
