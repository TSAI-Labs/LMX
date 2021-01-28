# Core Django imports.
from django.views.generic import ListView

# Blog application imports.
from lms.models.course_model import Course
from lms.models.profile_model import Profile
from django.shortcuts import render, Http404, HttpResponse

from django_filters import filterset
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "lms/course/home.html"



#dummy model 
from django_tables2 import SingleTableView, RequestConfig
from django_tables2.export.views import ExportMixin

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.export import TableExport
from lms.tables import StudentAssignmentTable, StudentAssignmentFilter
from lms.models.assignment_model import StudentAssignment

class GradeBookCourseView(ExportMixin, SingleTableMixin, FilterView):
    model = StudentAssignment
    table_class = StudentAssignmentTable
    
    template_name = 'lms/course/gradebook/course_gradebook.html'
    filterset_class  = StudentAssignmentFilter

    # def get(self, request, *args, **kwargs):
    #     # table = StudentAssignmentTable(StudentAssignment.objects.filter(assignment__name=kwargs[pk]))
    #     pass


# download csv file (django_tables2 method)
# def table_download(request):
#     table = StudentAssignmentTable(StudentAssignment.objects.all())

#     RequestConfig(request).configure(table)

#     export_format = request.GET.get("_export", None)
#     if TableExport.is_valid_format(export_format):
#         exporter = TableExport(export_format, table)
#         return exporter.response("table.{}".format(export_format))

#     return render(request, "lms/course/gradebook/course_gradebook_export.html", {
#         "table": table
#     })





