from django.db import models

from .recipe import Recipe


class Item(models.Model):
    url = models.CharField(max_length=200)
    body = models.CharField(max_length=500)
    order_number = models.IntegerField(blank=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ["order_number"]
        unique_together = ("recipe", "order_number")
