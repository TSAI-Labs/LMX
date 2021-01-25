# Core Django imports.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.forms import ModelForm
from django.urls import reverse_lazy

# Blog application imports.
from lms.models.assignment_model import Assignment, Comment


class DateInput(forms.DateInput):
    input_type = 'date'


class AssignmentHomeView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "assignments/home_assignment.html"
    ordering = ['-available_from']

class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "assignments/show_assignment.html"

class CreateForm(ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'


        widgets = {
            'due_date': DateInput(),
            'available_from': DateInput(),
            'until': DateInput(),
        }

class CommentForm(LoginRequiredMixin, ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    

class CommentCreateView(CreateView):
    model = Comment
    context_object_name = "comment"
    template_name = "assignments/create_comment.html"
    #fields = '__all__'
    form_class = CommentForm
    #success_url = reverse_lazy('home')
    success_url = '/'

    def form_valid(self, form):
        form.instance.assignment_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "assignments/create_assignment.html"
    form_class = CreateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # if user is author, then only make changes
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False

# Delete the assignments  
class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.created_by:
            return True
        return False

# Update the assignments
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    success_url = '/'
    template_name = "assignments/create_assignment.html"
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        assigment = self.get_object()

        if self.request.user == assigment.created_by:
            return True
        return False
