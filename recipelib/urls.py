from django.urls import path, include
from . import views

urlpatterns = [
  path('users/signup', views.UserSignup.as_view(), name='users'),
]
