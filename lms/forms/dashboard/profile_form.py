from django import forms

# LMS application imports.
from lms.models.student_model import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']