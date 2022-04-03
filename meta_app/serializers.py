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


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTeacherLesson
        fields = '__all__'
        depth = 1

