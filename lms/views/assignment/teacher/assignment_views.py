# Core Django imports.
from django.views.generic import ListView, DetailView, CreateView

# Blog application imports.
from lms.models.assignment_model import Assignment


class AssignmentListView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "lms/assignment/list_assignment.html"

class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "lms/assignment/show_assignment.html"

class AssignmentCreateView(CreateView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "lms/assignment/create_assignment.html"
    fields = '__all__'