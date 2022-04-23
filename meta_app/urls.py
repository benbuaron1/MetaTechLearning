from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [

    path('register',views.register),
    path('user/profile',views.user_profile),
    path('token/',obtain_auth_token),
    path('lessons', views.lesson_details),
    path('subject',views.user_subjects),
    path('subject/<str:name>',views.user_subjects),
    path('test/<str:pk>',views.single_test),
    path('current_user', views.current_user),
    path('get_teachers', views.get_teachers),
    path('get_students', views.get_students),
    path('get_subjects', views.get_subjects),
    path('test',views.tests),
    path('test_by_student',views.tests_by_student),
    path('all_users',views.get_all_users),
    path('user/getusertype', views.get_user_type),
    path('admin/get_un_approved', views.admin_get_unapproved_lessons),
    path('admin/approve', views.admin_approve_lesson)

    # path('stats', views.stats),
    # path('stats/<str:pk>', views.stats_per_student),
]