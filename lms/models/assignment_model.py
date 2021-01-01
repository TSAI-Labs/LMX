from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    #content = models.TextField()
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    #teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    #course 

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lms:assignment_detail', args=(str(self.id)))