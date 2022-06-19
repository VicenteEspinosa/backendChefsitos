from django.shortcuts import render

from recipelib.api_views.ingredient import IngredientView
from recipelib.api_views.measurement import MeasurementView
from recipelib.api_views.recipe import (
    FeedView,
    RateRecipeView,
    RecipeView,
    SelfRecipesView,
    SocialRecipesView,
)
from recipelib.api_views.tag import TagView
from recipelib.api_views.user import (
    SocialUserView,
    UserSignin,
    UserSignout,
    UserSignup,
    UserView,
)
