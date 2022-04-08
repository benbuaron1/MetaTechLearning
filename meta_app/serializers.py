from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',

        )

        extra_kwargs = {'password':{'write_only':True}}
        depth = 0

    def save(self):
        user = User(email=self.validated_data['email'],
                    username=self.validated_data['email'],
                    first_name=self.validated_data['first_name'],
                    last_name=self.validated_data['last_name'],
                    )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        depth = 1

    def save(self, type , **kwargs):
        newProfile = UserProfile(
            birth_date=self.validated_data['birth_date'],
                    phone_number=self.validated_data['phone_number'],
                    address=self.validated_data['address'],
                    user=self.instance,
                    type=type)
        newProfile.save()
        return newProfile




class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTeacherLesson
        fields = '__all__'
        depth = 1


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        depth = 1


class TestsExecutedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestExecuted
        fields = '__all__'
        depth = 1


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        depth = 1

    def save(self, **kwargs):
        newTeacher = Teacher(profile=self.instance)
        newTeacher.save()
        return newTeacher

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 1

    def save(self,**kwargs):
        newStudent = Student(profile=self.instance,
                            )
        newStudent.save()
        return newStudent


#     newProfile = UserProfile(birth_date=self.validated_data['birth_date'],
#                     phone_number=self.validated_data['phone_number'],
#                     address=self.validated_data['address'],
#                     user=self.instance)
#         newProfile.save()
#         return newProfile
