from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# LMS application imports.
from lms.models.student_model import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'user_tz']
