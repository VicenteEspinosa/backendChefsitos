from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    picture_url = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=200, blank=False)
    private = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
