# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from lms.forms.course.course_create_form import CourseCreateForm
from lms.models.assignment_model import StudentAssignment
from lms.models.course_model import Course, StudentCourse
from lms.models.user_role_model import Role
from lms.tables import StudentAssignmentTable, StudentAssignmentFilter, TeacherAssignmentTable, TeacherAssignmentFilter


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    context = {}
    template_name = "lms/course/course_home.html"

    def get(self, request, *args, **kwargs):

        role = Role.objects.filter(user=request.user)
        if role[0].is_student:
            selected_student_course = StudentCourse.objects.get(id=kwargs['pk'])
            print(selected_student_course)
            selected_course = Course.objects.get(id=selected_student_course.courses_id)
            print(selected_course)
            self.context.update(object1=selected_student_course)
            self.context.update(object=selected_course)
        else:
            selected_course = Course.objects.get(id=kwargs['pk'])
            self.context.update(object=selected_course)

        return render(request, self.template_name, self.context)


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Class View to create a new course
    """

    model = Course
    form_class = CourseCreateForm
    template_name = "lms/course/course_create.html"
    success_message = 'Course is successfully created!'

    # url to redirect to on success
    def get_success_url(self):
        return reverse('lms:dashboard_home')

    def get_initial(self, *args, **kwargs):
        initial = super(CourseCreateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CourseCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        if self.request.user.role.is_teacher:
            return True
        if self.request.user.role.is_teaching_assistant:
            return True
        return False

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


class GradeBookCourseView(LoginRequiredMixin, UserPassesTestMixin, ExportMixin, SingleTableMixin, FilterView):
    model = StudentAssignment
    table_class = TeacherAssignmentTable

    template_name = 'lms/course/gradebook/course_gradebook.html'
    filterset_class = TeacherAssignmentFilter

    def get_queryset(self):
        return StudentAssignment.objects.filter(assignment__for_course__id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['course_id'])
        return context

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_admin:
            return True
        elif self.request.user.role.is_teacher:
            return True
        elif self.request.user.role.is_teaching_assistant:
            return True
        return False

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')


class StudentGradeBookCourseView(LoginRequiredMixin, UserPassesTestMixin, ExportMixin, SingleTableMixin, FilterView):
    model = StudentAssignment
    table_class = StudentAssignmentTable

    template_name = 'lms/course/gradebook/course_gradebook.html'
    filterset_class = StudentAssignmentFilter

    def get_queryset(self):
        course_id = StudentCourse.objects.get(id=self.kwargs['course_id']).courses_id
        student_assignments = StudentAssignment.objects.filter(user=self.request.user)
        qs = [x.id for x in student_assignments if x.assignment.for_course_id == course_id]
        return StudentAssignment.objects.filter(id__in=qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object1'] = StudentCourse.objects.get(id=self.kwargs['course_id'])
        context['object'] = Course.objects.get(id=context['object1'].courses_id)
        return context

    # Restrict access to only course user (teacher) and admin
    def test_func(self):
        if self.request.user.role.is_student:
            return True
        return False

    # Redirect a logged in user, when they fail test_func()
    def handle_no_permission(self):
        messages.warning(self.request, 'Requested resource is not accessible!')
        return redirect('lms:dashboard_home')
