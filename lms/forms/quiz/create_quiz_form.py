from django import forms
from django.forms import ModelForm

from lms.models.quiz_model import Quiz


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateQuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

        widgets = {
            'Availablefrom': DateInput(),
            'Until': DateInput(),
            'created_by': forms.HiddenInput(),
            'course': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by')
        self.course = kwargs.pop('course')
        super(CreateQuizForm, self).__init__(*args, **kwargs)
