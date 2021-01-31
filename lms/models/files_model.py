
from datetime import datetime

# Core Django imports.
from django.db import models
from django.contrib.auth.models import User

from .course_model import Course

class File(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'files')
    name = models.CharField(max_length = 250, null = False, blank = False, unique = True)
    date_created = models.DateTimeField(default = datetime.now, blank = True)
    date_modified = models.DateTimeField(null = True, blank = True)
    modified_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'modified_by')
    file_uploaded = models.FileField(upload_to = 'uploaded_files')


