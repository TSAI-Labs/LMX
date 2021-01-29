# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

# Blog application imports.
from lms.forms.course.course_details_form import CourseDetailsForm
from lms.forms.course.course_section_forms import SectionForm, sections_choice_form, enrolled_students_formset, \
    get_unregistered_students_form
from lms.models.course_model import Course, Section, StudentCourse


class CourseDetailsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Class View to show / update the course_details for staff
    """

    model = Course
    form_class = CourseDetailsForm
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

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


class CourseSectionsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ['title']
    template_name = "lms/course/settings/course_sections_tab.html"

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
        context['sections_list_form'] = sections_choice_form(self.object)
        context['enrolled_students_formset'] = enrolled_students_formset(self.object)(instance=self.object)
        context['new_student_register_form'] = get_unregistered_students_form(self.object)()

        if self.request.POST:
            if self.request.POST.get('create-section'):
                context['section_create_form'] = SectionForm(self.request.POST)
            if self.request.POST.get('update-section'):
                context['sections_list_form'] = sections_choice_form()(self.request.POST)
                instance = Section.objects.get(id=int(self.request.POST['sections_list']))
                context['section_update_form'] = SectionForm(self.request.POST, instance=instance)
            if self.request.POST.get('update-section-assignments'):
                context['enrolled_students_formset'] = \
                    enrolled_students_formset(self.object)(self.request.POST, instance=self.object)

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

        if request.POST.get('new_student_register'):
            qs = StudentCourse.objects.filter(courses=self.object).filter(user=self.request.POST['user'])
            qs.update(registered='True')
            context['new_student_register_form'] = get_unregistered_students_form(self.object)()
            messages.success(request, 'New student is successfully registered!')

        context['enrolled_students_formset'] = enrolled_students_formset(self.object)(instance=self.object)
        context['new_student_register_form'] = get_unregistered_students_form(self.object)()

        return render(request, self.template_name, context=context)

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


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

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


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

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')
