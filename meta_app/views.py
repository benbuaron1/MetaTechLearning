from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db import IntegrityError, transaction
from django.db.models.base import ModelBase

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile, UserType, StudentTeacherLesson
from .serializers import *

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        with transaction.atomic():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                except IntegrityError as ex:
                    return Response(f"The email {request.data['email']} is already taken, try again",status.HTTP_400_BAD_REQUEST)
                user = User.objects.get(email=serializer.data['email'])
                type = UserType.objects.get(type=request.data['type'])
                newProfile = ProfileSerializer(instance=user,data=request.data)
                newUserToken = Token(user=user)
                newUserToken.save()
                if newProfile.is_valid():
                    profile = newProfile.save(type=type)
                    if request.data['type'] == 'student':
                        newStudent = StudentSerializer(instance=profile,data=request.data,partial=True)
                        if newStudent.is_valid():
                            newStudent.save()
                        else:
                            return Response(newStudent.errors)
                    elif request.data['type'] == 'teacher':
                        newTeacher = TeacherSerializer(instance=profile,data=request.data,partial=True)
                        if newTeacher.is_valid():
                            newTeacher.save()
                        else:
                            return Response(newTeacher.errors)
                else:
                    return Response(newProfile.errors,status.HTTP_400_BAD_REQUEST)
                return Response(data=serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_subject(request):
    if request.method == 'POST':
        student = Student.objects.get(profile__user=request.user)
        try:
            subject = Subject.objects.get(subject_name=request.data['subject'])
            student.subjects.add(subject)
            return Response('The subject added successfully',status.HTTP_201_CREATED)
        except:
            return Response(f"We dont support the subject {request.data['subject']} at the moment")

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
    # if request.method == 'GET':
    #     all_lessons = StudentTeacherLesson.objects.all()
    #     serializer = LessonSerializer(all_lessons,many=True)
    #     return Response(serializer.data,status.HTTP_200_OK)

    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        # print(user_profile)
        print(user_profile.type.type)
        if user_profile.type.type == 'teacher':
            with transaction.atomic():
                student = Student.objects.get(profile__user=request.data['student_id'])
                teacher = Teacher.objects.get(profile=user_profile)
                lesson = StudentTeacherLesson.objects.create(
                    student_id=student.id,
                    teacher_id=teacher.id,
                    subject=Subject.objects.get(subject_name=request.data['subject']),
                    lesson_date=request.data['lesson_date'],
                    lesson_material=request.data['lesson_material'],
                    record_url=request.data['record_url']
                )
                lesson.save()
                serializer = LessonSerializer(lesson)
                student.teachers.add(teacher)
                student.subjects.add(lesson.subject)
                teacher.students.add(student)
                return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


