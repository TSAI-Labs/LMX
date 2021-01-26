# Core Django imports.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from lms.models.assignment_model import StudentAssignment
from lms.models.course_model import Course , StudentCourse
from lms.tables import StudentAssignmentTable, StudentAssignmentFilter
from lms.models.user_role_model import Role


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    context={}
    template_name = "lms/course/home.html"
   

    # def get(self, request, *args, **kwargs):
    #     selected_course = Course.objects.get(id=kwargs['pk'])
    #     print(f'SELECTED COURSE {selected_course}')
    #     # selected_course.published=False
    #     # selected_course.save()
    #     return redirect('lms:dashboard_profile')

    def get(self, request, *args, **kwargs):
        
        role = Role.objects.filter(user=request.user)
        if role[0].is_student:
            selected_course = StudentCourse.objects.get(id=kwargs['pk'])
        else:
            selected_course = Course.objects.get(id=kwargs['pk'])
        self.context.update(object=selected_course)
        self.context.update(course_id=selected_course.id)
        self.context.update(is_student=role[0].is_student)
        
    # self.context.update(course_publish=selected_course.published)
        # self.context.update(course_description=selected_course.description)
        return render(request, self.template_name, self.context)
        

class CourseListView_default(ListView):
    model = Course
    context_object_name = "courses_default"
    template_name = "lms/lms_base.html"


class GradeBookCourseView(LoginRequiredMixin, UserPassesTestMixin, ExportMixin, SingleTableMixin, FilterView):
    model = StudentAssignment
    table_class = StudentAssignmentTable

    template_name = 'lms/course/gradebook/course_gradebook.html'
    filterset_class = StudentAssignmentFilter

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


# download csv file (django_tables2 method)
def table_download(request):
    table = StudentAssignmentTable(StudentAssignment.objects.all())

    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, "lms/course/gradebook/course_gradebook_export.html", {
        "table": table
    })
