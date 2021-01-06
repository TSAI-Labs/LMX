# Core Django imports.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.forms import ModelForm

# Blog application imports.
from assignments.models.assignment_model import Assignment


class DateInput(forms.DateInput):
    input_type = 'date'

class AssignmentBaseView(ListView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "base_assignment.html"

class AssignmentListView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "list_assignment.html"

class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "show_assignment.html"

class CreateForm(ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'
        widgets = {
            'due_date': DateInput(),
            'available_from': DateInput(),
            'until': DateInput(),
        }


class AssignmentCreateView(CreateView, ModelForm):
    model = Assignment
    context_object_name = "assignment"
    template_name = "create_assignment.html"
    #fields = '__all__'
    form_class = CreateForm

# Delete the assignments  
class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Assignment
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.user:
            return True
        return False

# Update the assignments
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    success_url = '/'
    fields = ['title', 'content']


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.user:
            return True
        return False