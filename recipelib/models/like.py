from django.contrib.auth.models import User
from django.db import models


class Like(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("recipe", "user")
