from django import forms
from django.forms import ModelForm
from lms.models.assignment_model import Assignment



class DateInput(forms.DateInput):
    input_type = 'date'

class CreateForm(ModelForm):
    class Meta:
        model = Assignment
        # fields = '__all__'
        fields = ['name', 'description',  'available_from', 'available_until', 'display_grades', 'sub_type', 'max_grade', 'image']

        widgets = {
            'available_from': DateInput(),
            'available_until': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('created_by')
        self.for_course = kwargs.pop('for_course')
        super(CreateForm, self).__init__(*args, **kwargs)
        print('I am from Init')


