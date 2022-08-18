# out sourced from https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/11-Pagination/django_project/blog/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lms:post-detail', kwargs={'pk': self.pk})
