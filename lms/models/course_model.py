# Core Django imports.
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

from lms.models.user_role_model import Role

class Course(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)
    #TODO change field type
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean(self):
        role = Role.objects.filter(user=self.user)
        if role:
            if not (role[0].is_admin or role[0].is_teacher):
                raise ValidationError("Only Teacher Or Admin Can Create Courses")
        else:
            raise ValidationError("Assign Role to the User")


class StudentCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentcourses')
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    registered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def clean(self):
        role = Role.objects.filter(user=self.user)
        if role:
            if (role[0].is_admin or role[0].is_teacher or role[0].is_teaching_assistant):
                raise ValidationError("Only Student can register to the courses")
        else:
            raise ValidationError("Assign Role to the User")

        if not self.courses.published:
            raise ValidationError("Only Published courses can be selected")

        student_courses = StudentCourse.objects.filter(user=self.user)
        if student_courses:
            if (self.courses in [stu_course.courses for stu_course in student_courses]):
                    raise ValidationError("Student already selected the course")
