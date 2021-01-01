# Core Django imports.
import pytz
from PIL import Image
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import ImageFieldFile, FileField
from django.utils import timezone


class GradingScheme(models.Model):
    """
    Model to capture various grading schemes.
    Courses will be able to choose from these grading schemes
    """
    scheme = models.CharField(max_length=250, null=False, blank=False, unique=True)

    def __str__(self):
        return f'Grading Scheme {self.scheme}'


class Course(models.Model):
    """
    Model to capture all the course details
    """
    title = models.CharField(max_length=250, null=False, blank=False, unique=True)
    thumbnail = models.ImageField(default='default.png', upload_to='course_thumbnails', null=True, blank=True)
    time_zone = models.CharField(max_length=35, choices=[(x, x) for x in pytz.common_timezones], default='Asia/Kolkata')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    grading_scheme = models.ForeignKey(to=GradingScheme, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    allow_self_enroll = models.BooleanField(default=True)
    enrollment_open_to_all = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} Course'

    # Resizing the image to 300x300, to save space on the web server
    def save(self, *args, **kwargs):

        if self.thumbnail.name == '':
            self.thumbnail = ImageFieldFile(instance=None, field=FileField(), name='default.png')
        else:
            img = Image.open(self.thumbnail.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

        super(Course, self).save(args, kwargs)

    # Perform validation
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be greater than the end date')


class Section(models.Model):
    """
    Students belonging to each course can be further sub-divided into sections
    """
    name = models.CharField(max_length=250, null=True, blank=False, unique=True)

    def __str__(self):
        return f'Section {self.name}'
