from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from lms.models.course_model import Course
from lms.models.user_role_model import Role


class DateInput(forms.DateInput):
    input_type = 'date'


def get_non_student_users():
    filtered_users = set()
    for user in list(User.objects.all()):
        role = Role.objects.filter(user=user)
        if role and not role[0].is_student:
            filtered_users.add(user.pk)
    return User.objects.filter(pk__in=filtered_users)


class CourseDetailsForm(ModelForm):
    user = forms.ModelChoiceField(queryset=get_non_student_users())

    class Meta:
        model = Course
        fields = ['title', 'thumbnail', 'start_date', 'end_date', 'grading_scheme', 'description',
                  'allow_self_enroll', 'published', 'user']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
