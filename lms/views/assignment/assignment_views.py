# Core Django imports.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.contrib.auth.models import User


# Blog application imports.
from lms.models.assignment_model import Assignment, Comment
from lms.models.course_model import Course

from lms.forms.assignment.create_assignment_form import CreateForm
from lms.forms.assignment.comment_form import CommentForm

from django.urls import reverse


class AssignmentHomeView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/home_assignment.html"
    ordering = ['-available_from']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id = self.kwargs['pkcourse'])
        return context
    
    def get_queryset(self):
          return Assignment.objects.filter(for_course = self.kwargs['pkcourse'])

class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/show_assignment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id = self.kwargs['pkcourse'])
        context['pk'] = self.kwargs['pk']
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',self.kwargs)
        return context
 


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/create_assignment.html"

    form_class = CreateForm #(initial={'created_by':  get_username, 'course':  self.request.user })

    # def get_username(self):
    #     return User.objects.get(username = self.request.user)

    # def get_course(self):
    #     return User.objects.get(username = self.request.user)

    def get_initial(self, *args, **kwargs):
        initial = super(AssignmentCreateView, self).get_initial(**kwargs)
        initial['created_by'] = User.objects.get(username = self.request.user)
        initial['for_course'] = Course.objects.get(id = self.kwargs['pkcourse'])
        print('##########$$$$$$$$$$$%%%%%%%%%%%%%^^^^^^^^^^^ Initial ', initial)
        return initial
    
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AssignmentCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['created_by'] = User.objects.get(username = self.request.user)
        kwargs['for_course'] = Course.objects.get(id = self.kwargs['pkcourse'])
        return kwargs

    # def get_initial(self):
    #     initial = super(AssignmentCreateView, self).get_initial()
    #     if self.request.user.is_authenticated:
    #         initial.update({'name': self.request.user.get_full_name()})
    #     return initial

    def form_valid(self, form):
        # course = Course.objects.get(id = self.kwargs['pkcourse'])
        # form.instance.for_course = course
        # print('##########$$$$$$$$^^^^^^^^^^**************', course)

        # print('##########$$$$$$$$^^^^^^^^^^**************', User.objects.get(username = self.request.user))

        # form.instance.created_by = User.objects.get(username = self.request.user)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id = self.kwargs['pkcourse'])
        return context

    def get_success_url(self):
        return reverse('lms:assignment_home', kwargs={'pkcourse':self.kwargs['pkcourse']})
    

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

    # LMX\lms\templates\assignments\assignment_confirm_delete.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Course.objects.get(id = self.kwargs['pkcourse'])
        return context

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False

# Update the assignments
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    context_object_name = "assignments"

    template_name = "assignments/create_assignment.html"
    fields = ['name', 'description', 'available_from', 'available_until', 'display_grades', 'sub_type', 'max_grade', 'image']

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
        context['object'] = Course.objects.get(id = self.kwargs['pkcourse'])
        return context
    
    def get_success_url(self):
        return reverse('lms:assignment_detail', kwargs={'pkcourse':self.kwargs['pkcourse'], 'pk': self.kwargs['pk']})
    

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
        context['object'] = Course.objects.get(id = self.kwargs['pkcourse'])
        context['assignments'] = Assignment.objects.get(id = self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return reverse('lms:assignment_detail', kwargs={'pkcourse':self.kwargs['pkcourse'], 'pk': self.kwargs['pk']})

    
    
