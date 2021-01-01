from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Staff(models.Model):
    """
    Model to capture the details of staff users. Admins, teachers and teaching assistants are considered as staff
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_teaching_assistant = models.BooleanField(default=False)

    def __str__(self):
        return f"Staff - {self.user.username}"

    def clean(self):
        # User must be assigned at least one role - admin, teacher, or teaching assistant
        if not (self.is_admin or self.is_teacher or self.is_teaching_assistant):
            raise ValidationError('Make at least one selection')

        # Verify if the user is already registered as a student
        if len(Student.objects.filter(user=self.user)) == 1:
            raise ValidationError('User is already registered as a student. Students cannot be included into staff')


class Student(models.Model):
    """
    Model to capture the details of students
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student - {self.user.username}"

    def clean(self):
        # Verify if the user is already registered as a teacher
        if len(Staff.objects.filter(user=self.user)) == 1:
            raise ValidationError('User is already registered as a staff. Staff cannot be included into students')