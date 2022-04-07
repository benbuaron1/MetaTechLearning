from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [

    path('register',views.register),
    path('user/profile',views.user_profile),
    path('token/',obtain_auth_token),
    path('lessons',views.Lesson_details),

]