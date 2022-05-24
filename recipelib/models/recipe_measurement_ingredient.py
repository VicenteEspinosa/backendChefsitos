from django.db import models


class RecipeMeasurementIngredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
    )
    measurement = models.ForeignKey(
        "Measurement",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        "Ingredient",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(blank=False)
