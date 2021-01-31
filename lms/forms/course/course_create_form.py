from django import forms
from django.forms import ModelForm

from lms.forms.course.course_details_form import DateInput
from lms.models.course_model import Course


class CourseCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CourseCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = ['title', 'thumbnail', 'start_date', 'end_date', 'grading_scheme', 'description',
                  'allow_self_enroll', 'published', 'user']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'user': forms.HiddenInput(),
        }
