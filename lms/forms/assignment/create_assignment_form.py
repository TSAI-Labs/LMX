from django import forms
from django.forms import ModelForm
from lms.models.assignment_model import Assignment


class DateInput(forms.DateInput):
    input_type = 'date'

class CreateForm(ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'


        widgets = {
            'due_date': DateInput(),
            'available_from': DateInput(),
            'until': DateInput(),
        }