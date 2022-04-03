from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, User
from django.utils import timezone


class MetaModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class UserType(MetaModel):
    type = models.CharField(max_length=128)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'UserTypes'

class UserProfile(MetaModel):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    # birth_date = models.DateTimeField(blank=True,null=True)
    credits = models.IntegerField(default=0)
    address = models.CharField(max_length=512,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    type = models.ForeignKey(UserType,on_delete=models.RESTRICT,null=True,blank=True)

    class Meta:
        db_table = 'UserProfiles'


class StudentTeacherLesson(MetaModel):
    student = models.ForeignKey(UserProfile,on_delete=models.RESTRICT,related_name='Student')
    teacher = models.ForeignKey(UserProfile,on_delete=models.RESTRICT,related_name='Teacher')
    subject = models.TextField(max_length=1028, null=False, blank=False)
    record_url = models.URLField(blank=True, null=True)
    lesson_date = models.DateField(null=False,blank=False)
    lesson_material = models.URLField(null=True,blank=True)

    def __str__(self):
        return f"{self.student} by {self.teacher} at {self.lesson_date}"

    class Meta:
        db_table = 'Lessons'




