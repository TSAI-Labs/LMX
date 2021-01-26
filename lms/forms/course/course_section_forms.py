from django import forms
from django.forms import ModelForm, inlineformset_factory

from lms.models.course_model import Section, StudentCourse, Course


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_name', 'course']
        widgets = {
            'course': forms.HiddenInput(),
        }


def sections_choice_form(course_obj):
    class SectionChoiceForm(forms.Form):
        sections_list = forms.ModelChoiceField(queryset=Section.objects.filter(course=course_obj))

    return SectionChoiceForm


def enrolled_students_formset(course_obj):
    class EnrollmentsForm(ModelForm):
        section = forms.ModelChoiceField(queryset=Section.objects.filter(course=course_obj), required=False)

        class Meta:
            model = StudentCourse
            fields = ['user', 'courses', 'registered', 'section']
            widgets = {
                'user': forms.HiddenInput(),
                'courses': forms.HiddenInput(),
            }

    enrollments = StudentCourse.objects.filter(courses=course_obj).filter(registered=True)
    total_num_forms = len(enrollments)
    enrollments_formset = inlineformset_factory(parent_model=Course, model=StudentCourse, form=EnrollmentsForm,
                                                extra=total_num_forms, min_num=total_num_forms,
                                                max_num=total_num_forms, validate_max=True, validate_min=True,
                                                can_delete=False,
                                                fields=['user', 'courses', 'registered', 'section'])

    return enrollments_formset
