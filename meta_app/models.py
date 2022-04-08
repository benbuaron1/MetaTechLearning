from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
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
    type = models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'UserTypes'

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    birth_date = models.DateTimeField(blank=True,null=True)
    address = models.CharField(max_length=512,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    type = models.ForeignKey(UserType,on_delete=models.RESTRICT,null=True,blank=True)

    class Meta:
        db_table = 'UserProfiles'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Subject(MetaModel):
    subject_name = models.CharField(max_length=512,null=False,blank=False)

    class Meta:
        db_table = 'Subjects'

    def __str__(self):
        return self.subject_name


class Teacher(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.RESTRICT)
    subjects = models.ManyToManyField(Subject,null=True,blank=True)
    credits = models.IntegerField(default=0,null=True,blank=True)
    students = models.ManyToManyField("Student",null=True,blank=True)

    class Meta:
        db_table = 'Teachers'


class Student(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.RESTRICT)
    subjects = models.ManyToManyField(Subject,null=True,blank=True)
    credits = models.IntegerField(default=0,null=True,blank=True)
    teachers = models.ManyToManyField("Teacher",null=True,blank=True)

    class Meta:
        db_table = 'Students'

    # def __str__(self):
    #     return f"{self.user.first_name} {self.user.last_name}"

class StudentTeacherLesson(MetaModel):
    student = models.ForeignKey(Student,on_delete=models.RESTRICT)
    teacher = models.ForeignKey(Teacher,on_delete=models.RESTRICT)
    subject = models.ForeignKey(Subject,on_delete=models.RESTRICT)
    record_url = models.URLField(blank=True, null=True)
    lesson_date = models.DateField(null=False,blank=False)
    lesson_material = models.URLField(null=True,blank=True)

    def __str__(self):
        return f"{self.student} by {self.teacher} at {self.lesson_date}"

    class Meta:
        db_table = 'Lessons'

class Test(MetaModel):
    name = models.CharField(max_length=64, null=False, blank=False)
    subject = models.CharField(max_length=32, null=False, blank=False)
    questions = models.ManyToManyField('Question', blank=True)


    class Meta:
        db_table = "Test"

    def __str__(self):
        return self.name


class Question(MetaModel):
    question = models.CharField(max_length=256, null=True, blank=True)
    option1 = models.CharField(max_length=256, null=True, blank=True)
    option2 = models.CharField(max_length=256, null=True, blank=True)
    option3 = models.CharField(max_length=256, null=True, blank=True)
    option4 = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "Question"

    def __str__(self):
        return self.question


class TestExecuted(MetaModel):
    user = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)
    test_id = models.ForeignKey(Test, on_delete=models.RESTRICT)
    correct = models.IntegerField(null=False, blank=False)
    wrong = models.IntegerField(null=False, blank=False)
    grade = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )

    class Meta:
        db_table = "TakenTests"




