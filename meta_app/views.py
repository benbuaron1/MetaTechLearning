from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import IntegrityError

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile, UserType, StudentTeacherLesson
from .serializers import *

@api_view(['GET','POST'])
def users(request):
    if request.method == 'GET':
        all_users = User.objects.all()
        serializer = UserSerializer(all_users,many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                # print(serializer)
            except IntegrityError as ex:
                return Response(f"The email {request.data['email']} is already taken, try again",status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=serializer.data['email'])
            print(user)
            newProfile = ProfileSerializer(instance=user,data=request.data)
            newUserToken = Token(user=user)
            newUserToken.save()
            print(newProfile)
            if newProfile.is_valid():
                newProfile.save()
            else:
                return Response(newProfile.errors,status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    curr_user = request.user
    data = {
        "first_name": curr_user.first_name,
        "last_name" : curr_user.last_name
    }
    return Response(data)


@api_view(['GET','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Works good.
    :param request:
    :return:
    """
    try:
        user = UserProfile.objects.get(id=request.user.id)
        print('Found user')
    except:
        user = UserProfile(user_id=request.user.id)
        print('user')
        user.save()
    if request.method == 'PUT':
        serializer = ProfileSerializer(instance=user,data=request.data['profile'])
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
        serializer = ProfileSerializer(UserProfile.objects.all(),many=True)
        return Response(serializer.data)

@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Lesson_details(request):

    if request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        # print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        return Response(serializer.errors)

        # StudentTeacherLesson.objects.create(**data)
        # return Response(data,status.HTTP_201_CREATED)

    elif request.method == 'GET':
        all_lessons = StudentTeacherLesson.objects.all()
        serializer = LessonSerializer(all_lessons,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# in lesson details there is an error while trying to add lesson. need to be fixed with the serializer

