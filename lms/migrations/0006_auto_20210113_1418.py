# Generated by Django 3.1.4 on 2021-01-13 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_profile_timezone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='timezone',
            new_name='user_tz',
        ),
    ]
