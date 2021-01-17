# Core Django imports.
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ModelForm, inlineformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

# Blog application imports.
from lms.forms.course.course_section_forms import SectionForm
from lms.models.course_model import Course, Section
from lms.models.enrollment_model import Enrollment
from lms.models.users_model import Staff


class CourseDetailsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Class View to show / update the course_details for staff
    """

    model = Course
    fields = ['title', 'thumbnail', 'time_zone', 'start_date', 'end_date', 'grading_scheme', 'description',
              'allow_self_enroll', 'enrollment_open_to_all']
    template_name = "lms/course/settings/course_details_tab.html"
    success_message = 'Course details have been successfully updated!'

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_details', kwargs={'pk': self.object.pk})

    # Restrict access to only staff members
    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1


class CourseSectionsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ['title']
    template_name = "lms/course/settings/course_sections_tab.html"

    def sections_choice_form(self):
        class SectionChoiceForm(forms.Form):
            sections_list = forms.ModelChoiceField(queryset=Section.objects.filter(course=self.object))

        return SectionChoiceForm

    def enrolled_students_formset(self, post=None):

        class EnrollmentsForm(ModelForm):
            section = forms.ModelChoiceField(queryset=Section.objects.filter(course=self.object), required=False)

            class Meta:
                model = Enrollment
                fields = ['student', 'course', 'section']
                widgets = {
                    'student': forms.HiddenInput(),
                    'course': forms.HiddenInput(),
                }

        enrollments = Enrollment.objects.filter(course=self.object)
        total_num_forms = len(enrollments)
        enrollments_formset = inlineformset_factory(parent_model=Course, model=Enrollment, form=EnrollmentsForm,
                                                    extra=total_num_forms, min_num=total_num_forms,
                                                    max_num=total_num_forms, validate_max=True, validate_min=True,
                                                    can_delete=False, fields=['student', 'course', 'section'])

        initial = []
        for enrollment in enrollments:
            initial.append({
                'student': enrollment.student,
                'section': enrollment.section
            })

        if post:
            formset = enrollments_formset(post, instance=self.object)
        else:
            formset = enrollments_formset(instance=self.object)

        return formset

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_sections', kwargs={'pk': self.object.pk})

    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1

    def get_context_data(self, **kwargs):
        context = super(CourseSectionsView, self).get_context_data()
        context['section_create_form'] = SectionForm(initial={'course': self.object})
        context['section_update_form'] = SectionForm(initial={'course': self.object})
        context['sections_list_form'] = self.sections_choice_form()
        context['enrolled_students_formset'] = self.enrolled_students_formset()

        if self.request.POST:
            if self.request.POST.get('create-section'):
                context['section_create_form'] = SectionForm(self.request.POST)
            if self.request.POST.get('update-section'):
                context['sections_list_form'] = self.sections_choice_form()(self.request.POST)
                instance = Section.objects.get(id=int(self.request.POST['sections_list']))
                context['section_update_form'] = SectionForm(self.request.POST, instance=instance)
            if self.request.POST.get('update-section-assignments'):
                context['enrolled_students_formset'] = self.enrolled_students_formset(self.request.POST)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        if request.POST.get('create-section'):
            form = context['section_create_form']
            if form.is_valid():
                form.save()
                messages.success(request, 'New Section successfully created!')

        if request.POST.get('update-section'):
            form = context['section_update_form']
            if form.is_valid():
                form.save()
                messages.success(request, 'Section successfully updated!')

        if request.POST.get('delete-section'):
            instance = Section.objects.get(id=int(self.request.POST['sections_list']))
            instance.delete()
            messages.success(request, 'Section successfully deleted!')

        if request.POST.get('update-section-assignments'):
            for form_data in context['enrolled_students_formset'].cleaned_data:
                _id = form_data['id']
                del form_data['id']
                if _id and Enrollment.objects.filter(id=_id.id):
                    Enrollment.objects.filter(id=_id.id).update(**form_data)
            messages.success(request, 'Student sections successfully updated!')

        return render(request, self.template_name, context=context)


# todo: full implementation
class CourseManageView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ['title']
    template_name = "lms/course/settings/course_manage_tab.html"

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_sections', kwargs={'pk': self.object.pk})

    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1


# todo: full implementation
class CourseStatisticsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DetailView):
    model = Course
    template_name = "lms/course/settings/course_statistics_tab.html"

    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1
