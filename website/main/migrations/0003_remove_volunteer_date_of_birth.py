# Generated by Django 5.0 on 2023-12-16 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_project_work_type_application_task_volunteer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='date_of_birth',
        ),
    ]
