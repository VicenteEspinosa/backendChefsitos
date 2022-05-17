from django.urls import path, include
from . import views

urlpatterns = [
  path('measurements/', views.MeasurementView.as_view(), name='measurements'),
  path('measurements/<int:measurement_id>/', views.MeasurementView.as_view(), name='measurements'),
  path('users/signup/', views.UserSignup.as_view(), name='user_signup'),
  path('users/signin/', views.UserSignin.as_view(), name='user_signin'),
  path('users/signout/', views.UserSignout.as_view(), name='user_signout')
]
