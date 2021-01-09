# Core Django imports.
from django.views.generic import ListView

# Blog application imports.
from lms.models.course_model import Course


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "lms/course/home.html"