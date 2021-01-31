# Generated by Django 3.1.4 on 2021-01-21 21:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lms', '0015_studentcourse_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='user',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='studentcourse',
            unique_together={('user', 'courses')},
        ),
        migrations.DeleteModel(
            name='Enrollment',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
