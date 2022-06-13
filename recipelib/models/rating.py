from django.contrib.auth.models import User
from django.db import models


class Rating(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ("recipe", "user")
