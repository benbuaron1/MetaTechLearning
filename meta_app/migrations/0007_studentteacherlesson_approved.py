# Generated by Django 4.0.3 on 2022-04-22 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta_app', '0006_studentteacherlesson_student_full_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentteacherlesson',
            name='approved',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
