from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [

    path('register',views.register),
    path('user/profile',views.user_profile),
    path('token/',obtain_auth_token),
    path('lessons', views.lesson_details),
    path('subject',views.add_subject),
    path('test/<str:pk>',views.single_test),
    path('current_user', views.current_user),
    # path('stats', views.stats),
    # path('stats/<str:pk>', views.stats_per_student),
]