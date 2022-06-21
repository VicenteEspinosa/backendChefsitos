from django.urls import include, path

from . import views

urlpatterns = [
    path("recipes/", views.RecipeView.as_view(), name="recipes"),
    path(
        "recipes/self/", views.SelfRecipesView.as_view(), name="self_recipes"
    ),
    path("recipes/feed/", views.FeedView.as_view(), name="feed"),
    path(
        "recipes/feed/following/",
        views.FollowingFeedView.as_view(),
        name="following_feed",
    ),
    path(
        "recipes/<int:recipe_id>/rate/",
        views.RateRecipeView.as_view(),
        name="rate",
    ),
    path(
        "recipes/<int:recipe_id>/",
        views.RecipeView.as_view(),
        name="recipes",
    ),
    path(
        "recipes/chef/<int:user_id>/",
        views.SocialRecipesView.as_view(),
        name="chef_recipes",
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
    path("tags/", views.TagView.as_view(), name="tags"),
    path(
        "tags/<int:tag_id>/",
        views.TagView.as_view(),
        name="tags",
    ),
    path(
        "users/<int:user_id>/follow/",
        views.UserFollow.as_view(),
        name="user_follow",
    ),
    path("users/signup/", views.UserSignup.as_view(), name="user_signup"),
    path("users/signin/", views.UserSignin.as_view(), name="user_signin"),
    path("users/signout/", views.UserSignout.as_view(), name="user_signout"),
    path("users/show/", views.UserView.as_view(), name="user_view"),
    path(
        "users/show/<int:user_id>/",
        views.SocialUserView.as_view(),
        name="user_show_by_id",
    ),
    path("users/edit/", views.UserView.as_view(), name="user_edit"),
    path("users/delete/", views.UserView.as_view(), name="user_delete"),
]
