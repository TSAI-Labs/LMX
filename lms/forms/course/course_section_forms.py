from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet

from lms.models.course_model import Section, StudentCourse, Course, CourseSubscribe


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_name', 'course']
        widgets = {
            'course': forms.HiddenInput(),
        }


def get_unregistered_students_form(course_obj):
    filtered_users = set()
    qs = StudentCourse.objects.filter(courses=course_obj).filter(registered=False)
    for item in qs:
        filtered_users.add(item.user.pk)
    qs = User.objects.filter(pk__in=filtered_users)

    class UnregisteredStudentsForm(ModelForm):
        user = forms.ModelChoiceField(queryset=qs, required=True)

        class Meta:
            model = StudentCourse
            fields = ['user']

    return UnregisteredStudentsForm


def sections_choice_form(course_obj):
    class SectionChoiceForm(forms.Form):
        sections_list = forms.ModelChoiceField(queryset=Section.objects.filter(course=course_obj))

    return SectionChoiceForm


def enrolled_students_formset(course_obj):
    class EnrollmentsForm(ModelForm):
        section = forms.ModelChoiceField(queryset=Section.objects.filter(course=course_obj), required=False)

        class Meta:
            model = StudentCourse
            fields = ['user', 'registered', 'section']
            widgets = {
                'user': forms.HiddenInput(),
            }

    enrollments = StudentCourse.objects.filter(courses=course_obj).filter(registered=True)

    class EnrollmentsFormSet(BaseInlineFormSet):
        def __init__(self, *args, **kwargs):
            kwargs['queryset'] = enrollments
            super(EnrollmentsFormSet, self).__init__(*args, **kwargs)

    enrollments_formset = inlineformset_factory(parent_model=Course, model=StudentCourse,
                                                form=EnrollmentsForm,
                                                formset=EnrollmentsFormSet,
                                                extra=0, can_delete=False)

    return enrollments_formset

class CourseSubscribeForm(ModelForm):
    class Meta:
        model = CourseSubscribe
        fields = ['email_id', 'course']