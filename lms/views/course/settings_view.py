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
from lms.models.course_model import Course, Section, StudentCourse


class CourseDetailsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Class View to show / update the course_details for staff
    """

    model = Course
    fields = ['title', 'thumbnail', 'start_date', 'end_date', 'grading_scheme', 'description',
              'allow_self_enroll', 'published', 'user']
    template_name = "lms/course/settings/course_details_tab.html"
    success_message = 'Course details have been successfully updated!'

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_details', kwargs={'pk': self.object.pk})

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user == self.get_object().user:
            return True
        return False


class CourseSectionsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ['title']
    template_name = "lms/course/settings/course_sections_tab.html"

    def sections_choice_form(self):
        class SectionChoiceForm(forms.Form):
            sections_list = forms.ModelChoiceField(queryset=Section.objects.filter(course=self.object))

        return SectionChoiceForm

    def enrolled_students_formset(self):

        class EnrollmentsForm(ModelForm):
            section = forms.ModelChoiceField(queryset=Section.objects.filter(course=self.object), required=False)

            class Meta:
                model = StudentCourse
                fields = ['user', 'courses', 'registered', 'section']
                widgets = {
                    'user': forms.HiddenInput(),
                    'courses': forms.HiddenInput(),
                }

        enrollments = StudentCourse.objects.filter(courses=self.object)
        total_num_forms = len(enrollments)
        enrollments_formset = inlineformset_factory(parent_model=Course, model=StudentCourse, form=EnrollmentsForm,
                                                    extra=total_num_forms, min_num=total_num_forms,
                                                    max_num=total_num_forms, validate_max=True, validate_min=True,
                                                    can_delete=False,
                                                    fields=['user', 'courses', 'registered', 'section'])

        return enrollments_formset

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_sections', kwargs={'pk': self.object.pk})

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user == self.get_object().user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(CourseSectionsView, self).get_context_data()
        context['section_create_form'] = SectionForm(initial={'course': self.object})
        context['section_update_form'] = SectionForm(initial={'course': self.object})
        context['sections_list_form'] = self.sections_choice_form()
        context['enrolled_students_formset'] = self.enrolled_students_formset()(instance=self.object)

        if self.request.POST:
            if self.request.POST.get('create-section'):
                context['section_create_form'] = SectionForm(self.request.POST)
            if self.request.POST.get('update-section'):
                context['sections_list_form'] = self.sections_choice_form()(self.request.POST)
                instance = Section.objects.get(id=int(self.request.POST['sections_list']))
                context['section_update_form'] = SectionForm(self.request.POST, instance=instance)
            if self.request.POST.get('update-section-assignments'):
                context['enrolled_students_formset'] = \
                    self.enrolled_students_formset()(self.request.POST, instance=self.object)

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
                if _id and StudentCourse.objects.filter(id=_id.id):
                    StudentCourse.objects.filter(id=_id.id).update(**form_data)
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

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user == self.get_object().user:
            return True
        return False


# todo: full implementation
class CourseStatisticsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DetailView):
    model = Course
    fields = ['title']

    template_name = "lms/course/settings/course_statistics_tab.html"

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user == self.get_object().user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(CourseStatisticsView, self).get_context_data()
        context['total_students'] = len(StudentCourse.objects.filter(courses=self.object))
        context['total_registered_students'] = len(StudentCourse.objects.filter(courses=self.object, registered=True))
        context['total_unregistered_students'] = len(
            StudentCourse.objects.filter(courses=self.object, registered=False))
        context['total_sections'] = len(Section.objects.filter(course=self.object))
        return context
