from django import forms
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from lms.models.assignment_model import Comment

class CommentForm(LoginRequiredMixin, ModelForm):
    class Meta:
        model = Comment
        fields = ['content']