# Generated by Django 4.0.3 on 2022-04-03 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meta_app', '0003_usertype_userprofile_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTeacherLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('subject', models.TextField(max_length=1028)),
                ('record_url', models.URLField(blank=True, null=True)),
                ('lesson_date', models.DateField()),
                ('lesson_material', models.URLField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='Student', to='meta_app.userprofile')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='Teacher', to='meta_app.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]