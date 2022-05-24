from django.contrib.auth.models import User
from django.db import models

from recipelib.models.ingredient import Ingredient
from recipelib.models.measurement import Measurement
from recipelib.models.tag import Tag


class Recipe(models.Model):
    picture_url = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    name = models.CharField(max_length=200, blank=False)
    private = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    measurements = models.ManyToManyField(
        Measurement, through="RecipeMeasurementIngredient"
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeMeasurementIngredient"
    )
    tags = models.ManyToManyField(Tag, through="RecipeTag")
