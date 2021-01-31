# Core Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from lms.forms.assignment.comment_form import CommentForm
from lms.forms.assignment.create_assignment_form import CreateForm
from lms.models.assignment_model import Assignment, Comment, StudentAssignment
from lms.models.course_model import Course, StudentCourse


class AssignmentHomeView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/home_assignment.html"
    ordering = ['-available_from']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return context

    def get_queryset(self):
        return Assignment.objects.filter(for_course=self.kwargs['pkcourse'])


class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/show_assignment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['pkcourse'])
        context['pk'] = self.kwargs['pk']
        return context


class AssignmentHomeStudentView(ListView):
    model = StudentAssignment
    context_object_name = "assignments"
    template_name = "assignments/home_assignment.html"
    ordering = ['-available_from']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object1'] = StudentCourse.objects.get(id=self.kwargs['pkcourse'])
        context['object'] = Course.objects.get(id=context['object1'].courses_id)
        context['is_student_view'] = True
        return context

    def get_queryset(self):
        course_id = StudentCourse.objects.get(id=self.kwargs['pkcourse']).courses_id
        student_assignments = StudentAssignment.objects.filter(user=self.request.user)
        qs = [x.id for x in student_assignments if x.assignment.for_course_id == course_id]
        return StudentAssignment.objects.filter(id__in=qs)


class AssignmentDetailStudentView(DetailView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/show_assignment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object1'] = StudentCourse.objects.get(id=self.kwargs['pkcourse'])
        context['object'] = Course.objects.get(id=context['object1'].courses_id)
        context['pk'] = self.kwargs['pk']
        context['is_student_view'] = True
        return context

    # def get_queryset(self):
    #     qs = []
    #     student_course = StudentCourse.objects.get(id=self.kwargs['pkcourse'])
    #     for item in StudentAssignment.objects.filter(user=self.request.user):
    #         if item.assignment.for_course_id == student_course.courses_id:
    #             qs.append(item.id)
    #     return StudentAssignment.objects.filter(id__in=qs)


class AssignmentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/create_assignment.html"
    success_message = "Assignment successfully created!"

    form_class = CreateForm

    def get_initial(self, *args, **kwargs):
        initial = super(AssignmentCreateView, self).get_initial(**kwargs)
        initial['created_by'] = User.objects.get(username=self.request.user)
        initial['for_course'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AssignmentCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['created_by'] = User.objects.get(username=self.request.user)
        kwargs['for_course'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return context

    def get_success_url(self):
        return reverse('lms:assignment_home', kwargs={'pkcourse': self.kwargs['pkcourse']})

    # if user is author, then only make changes
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False


# Delete the assignments
class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    template_name = "assignments/assignment_confirm_delete.html"
    context_object_name = "assignments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return context

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False

    def get_success_url(self):
        return reverse('lms:assignment_home', kwargs={'pkcourse': self.kwargs['pkcourse']})


# Update the assignments
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    context_object_name = "assignments"

    form_class = CreateForm

    template_name = "assignments/create_assignment.html"

    def get_initial(self, *args, **kwargs):
        initial = super(AssignmentUpdateView, self).get_initial(**kwargs)
        initial['created_by'] = User.objects.get(username=self.request.user)
        initial['for_course'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AssignmentUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['created_by'] = User.objects.get(username=self.request.user)
        kwargs['for_course'] = Course.objects.get(id=self.kwargs['pkcourse'])
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        assigment = self.get_object()

        if self.request.user == assigment.created_by:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['pkcourse'])
        context['is_update_view'] = True
        return context

    def get_success_url(self):
        return reverse('lms:assignment_detail', kwargs={'pkcourse': self.kwargs['pkcourse'], 'pk': self.kwargs['pk']})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    context_object_name = "comment"
    template_name = "assignments/create_comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.assignment_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id=self.kwargs['pkcourse'])
        context['assignments'] = Assignment.objects.get(id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('lms:assignment_detail', kwargs={'pkcourse': self.kwargs['pkcourse'], 'pk': self.kwargs['pk']})
