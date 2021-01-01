# Core Django imports.
from django.db import models

from .course_model import Course, Section
from .users_model import Student


class Enrollment(models.Model):
    """
    Model to capture student-course enrollments.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.student.user.username} enrolled in {self.course.title}'

    # Constraints to ensure that a student cannot enroll into the same course more than once
    class Meta:
        unique_together = ('student', 'course',)
