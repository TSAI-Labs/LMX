from django import forms
from django.forms import ModelForm

from lms.models.course_model import Section


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_name', 'course']
        widgets = {
            'course': forms.HiddenInput(),
        }


