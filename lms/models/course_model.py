# Core Django imports.
import pytz
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from lms.models.user_role_model import Role


class GradingSchemeName(models.Model):
    """
    Model to capture various grading schemes.
    Courses will be able to choose from these grading schemes
    """
    name = models.CharField(max_length=250, null=False, blank=False, unique=True)

    def __str__(self):
        return f'Grading Scheme {self.name}'


class GradingScheme(models.Model):
    """
    Model to capture various grading schemes.
    Courses will be able to choose from these grading schemes
    """
    scheme_name = models.ForeignKey(to=GradingSchemeName, on_delete=models.CASCADE)
    grade = models.CharField(max_length=250, null=False, blank=False)
    score_range_begin = models.SmallIntegerField()
    score_range_end = models.SmallIntegerField()

    def __str__(self):
        return f'{self.scheme_name}, Grade: {self.grade}, Scores: [{self.score_range_begin}, {self.score_range_end})'

    def clean(self):
        super(GradingScheme, self).clean()

        if self.score_range_end and self.score_range_begin:
            if self.score_range_end < self.score_range_begin:
                raise ValidationError('Range Error: Score end value is less that the score begin value!')

    # # Constraints to ensure that a duplicate entry is not present with scheme name and grade
    # class Meta:
    #     unique_together = ('scheme_name', 'grade',)


class Course(models.Model):
    """
    Model to capture all the course details
    """
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)
    # TODO change field type
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(null=True)
    published = models.BooleanField(default=False)

    thumbnail = models.ImageField(default='default.png', upload_to='course_thumbnails', null=True, blank=True)
    # time_zone=models.CharField(max_length=35, choices=[(x, x) for x in pytz.common_timezones], default='Asia/Kolkata')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    grading_scheme = models.ForeignKey(to=GradingSchemeName, on_delete=models.SET_NULL, null=True, blank=True)
    allow_self_enroll = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def clean(self):
        role = Role.objects.filter(user=self.user)
        if role:
            if not (role[0].is_admin or role[0].is_teacher):
                raise ValidationError("Only Teacher Or Admin Can Create Courses")
        else:
            raise ValidationError("Assign Role to the User")

        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be greater than the end date')


class Section(models.Model):
    """
    Students belonging to each course can be further sub-divided into sections
    """
    section_name = models.CharField(max_length=250, null=True, blank=False, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'Section {self.section_name} - {self.course}'

    # Constraints to ensure that a duplicate entry is not present with section_name and course
    class Meta:
        unique_together = ('section_name', 'course',)


class StudentCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='studentcourses')
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True)
    registered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} is associated with {self.courses.title}'

    def clean(self):
        role = Role.objects.filter(user=self.user)
        if role:
            if role[0].is_admin or role[0].is_teacher or role[0].is_teaching_assistant:
                raise ValidationError("Only Student can register to the courses")
        else:
            raise ValidationError("Assign Role to the User")

        if not self.courses.published:
            raise ValidationError("Only Published courses can be selected")

    # Constraints to ensure that a student cannot enroll into the same course more than once
    class Meta:
        unique_together = ('user', 'courses',)


