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
from .custom_queries import *

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
                    return Response(status=405)
                user = User.objects.get(email=serializer.data['email'])
                type = UserType.objects.get(type=request.data['type'])
                new_profile = ProfileSerializer(instance=user, data=request.data)
                new_user_token = Token(user=user)
                new_user_token.save()
                if new_profile.is_valid():
                    profile = new_profile.save(type=type)
                    if request.data['type'] == 'student':
                        new_student = StudentSerializer(instance=profile, data=request.data, partial=True)
                        if new_student.is_valid():
                            new_student.save()
                        else:
                            return Response(new_student.errors)
                    elif request.data['type'] == 'teacher':
                        new_teacher = TeacherSerializer(instance=profile, data=request.data, partial=True)
                        if new_teacher.is_valid():
                            new_teacher.save()
                        else:
                            return Response(new_teacher.errors)
                else:
                    return Response(new_profile.errors, status.HTTP_400_BAD_REQUEST)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_subject(request):
    if request.method == 'POST':
        student = Student.objects.get(profile__user=request.user)
        try:
            subject = Subject.objects.get(subject_name=request.data['subject'])
            student.subjects.add(subject)
            return Response('The subject added successfully', status.HTTP_201_CREATED)
        except:
            return Response(f"We dont support the subject {request.data['subject']} at the moment")


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    curr_user = request.user
    data = {
        "first_name": curr_user.first_name,
        "last_name": curr_user.last_name
    }
    return Response(data)


@api_view(['GET', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if user_profile.type.type == 'student':
            serializer = StudentSerializer(Student.objects.get(profile=user_profile))
            return Response(serializer.data)
        elif user_profile.type.type == 'teacher':
            serializer = TeacherSerializer(Teacher.objects.get(profile=user_profile))
            return Response(serializer.data)

    if request.method == 'PATCH':
        user = User.objects.get(id=request.user.id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        profile = UserProfile.objects.get(user=request.user)
        profile.address = request.data['address']
        profile.phone_number = request.data['phone_number']
        user.save()
        profile.save()
        return Response(status.HTTP_200_OK)

@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lesson_details(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
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
                    record_url=request.data['record_url'],
                    length=request.data['length']
                )
                current_student_credits = int(student.credits)
                credits_to_add = int(request.data['length']) // 6
                student.credits = current_student_credits + credits_to_add
                student.save()

                current_teacher_credits = int(teacher.credits)
                teacher.credits = current_teacher_credits + credits_to_add
                teacher.save()

                lesson.save()
                serializer = LessonSerializer(lesson)
                student.teachers.add(teacher)
                student.subjects.add(lesson.subject)
                teacher.students.add(student)
                return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'GET':
        if user_profile.type.type == 'teacher':
            teacher = Teacher.objects.get(profile=user_profile)
            serializer = LessonSerializer(StudentTeacherLesson.objects.filter(teacher=teacher), many=True)
            return Response(serializer.data)
        elif user_profile.type.type == 'student':
            student = Student.objects.get(profile=user_profile)
            serializer = LessonSerializer(StudentTeacherLesson.objects.filter(student=student), many=True)
            return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_teachers(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        if user_profile.type.type == 'student':
            student = Student.objects.get(profile=user_profile)
            serializer = LessonSerializer(StudentTeacherLesson.objects.filter(student=student).distinct('teacher_id'), many=True)
            nserializer = TeacherSerializer(student.teachers.distinct(),many=True)

            return Response(nserializer.data)



@api_view(['GET'])
def tests(request):
    if request.method == 'GET':
        all_tests = Test.objects.all()
        serializer = TestsSerializer(all_tests, many=True)
        return Response(data=serializer.data)



super_user_methods = ['PUT', 'PATCH', 'DELETE']

@api_view(['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
@authentication_classes([TokenAuthentication])
def single_test(request, pk):
    try:
        test = Test.objects.get(id=pk)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestsSerializer(test)
        return Response(data=serializer.data)

    elif request.method in super_user_methods:
        try:
            user = User.objects.get(id=request.user.id)
        except:
            return Response(status.HTTP_403_FORBIDDEN)
        if user.is_superuser == True:
            if request.method == 'PUT':
                serializer = TestsSerializer(test, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'PATCH':
                serializer = TestsSerializer(test, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif request.method == 'DELETE':
                test.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        answers = request.data
        answers = dict(answers)
        count = 0
        total = 0
        for q in test.questions.all():
            total += 1
            for i, j in answers.items():
                if int(q.id) == int(i):
                    if q.option1 == j[0]:
                        count += 1
        try:
            student = Student.objects.get(profile__user=request.user)
            executed = TestExecuted.objects.create(
                student=student,
                test_id=Test.objects.get(id=test.id),
                correct=count,
                wrong=total - count,
                grade=(count / total) * 100
            )
            executed.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(f"""
            You had {count} correct answers out of {total} total questions 
            in {test.name} test.
            Your grade is {(count / total) * 100}.
            Sign up to save results!
            """)



# TODO: update all the fields in the custom queries according to the changes

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def stats(request):
#     if 'sort' in request.GET:
#         ret = average_all_sorted()
#     else:
#         ret = average_all()
#     return Response(ret, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def stats_per_student(request, pk):
#     ret = average_student(pk)
#     return Response(ret, status=status.HTTP_200_OK)
