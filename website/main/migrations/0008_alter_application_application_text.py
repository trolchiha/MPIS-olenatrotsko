# Generated by Django 5.0 on 2023-12-17 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_application_application_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
