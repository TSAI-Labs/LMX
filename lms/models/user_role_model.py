from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Role(models.Model):
    """
    Model to capture the details of staff users. Admins, teachers and teaching assistants are considered as staff
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_teaching_assistant = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} role"

    def clean(self):
        # User must be assigned at least one role - admin, teacher, or teaching assistant or student
        if not (self.is_admin or self.is_teacher or self.is_teaching_assistant or self.is_student):
            raise ValidationError('Make at least one selection')

        # Verify if the user is already registered as a student
        if ((self.is_admin and self.is_student) or
            (self.is_teacher and self.is_student) or
            (self.is_teaching_assistant and self.is_student)):
            raise ValidationError('User can be either teacher or student. Choose one.')

    def save(self, *args, **kwargs):
        if self.is_admin:
            user = User.objects.get(username=self.user.username)
            user.is_staff = True
            print(user.is_staff)
        super().save(*args, **kwargs)
