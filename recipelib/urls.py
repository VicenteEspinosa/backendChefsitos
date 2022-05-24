from django.urls import include, path

from . import views

urlpatterns = [
    path("recipes/", views.RecipeView.as_view(), name="recipes"),
    path(
        "recipes/self/", views.SelfRecipesView.as_view(), name="self_recipes"
    ),
    path("ingredients/", views.IngredientView.as_view(), name="ingredients"),
    path(
        "ingredients/<int:ingredient_id>/",
        views.IngredientView.as_view(),
        name="ingredients",
    ),
    path(
        "measurements/", views.MeasurementView.as_view(), name="measurements"
    ),
    path(
        "measurements/<int:measurement_id>/",
        views.MeasurementView.as_view(),
        name="measurements",
    ),
    path("users/signup/", views.UserSignup.as_view(), name="user_signup"),
    path("users/signin/", views.UserSignin.as_view(), name="user_signin"),
    path("users/signout/", views.UserSignout.as_view(), name="user_signout"),
    path("users/show/", views.UserView.as_view(), name="user_view"),
    path("users/edit/", views.UserView.as_view(), name="user_edit"),
    path("users/delete/", views.UserView.as_view(), name="user_edit"),
]
