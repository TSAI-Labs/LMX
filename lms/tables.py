# lms/tables.py
import django_tables2 as tables
from lms.models.assignment_model import StudentAssignment

class TeacherAssignmentTable(tables.Table):
    class Meta:
        model = StudentAssignment
        template_name = "django_tables2/bootstrap4.html"
        
        fields = ('user', 'assignment__name','user__email', 'marks', 'assignment__max_grade',)

import django_filters

class TeacherAssignmentFilter(django_filters.FilterSet):
    class Meta:
        model = StudentAssignment
        fields = ['user', 'user__email', 'assignment__name']

class StudentAssignmentTable(tables.Table):
    class Meta:
        model = StudentAssignment
        template_name = "django_tables2/bootstrap4.html"
        
        fields = ( 'assignment__name', 'marks', 'assignment__max_grade',)


class StudentAssignmentFilter(django_filters.FilterSet):
    class Meta:
        model = StudentAssignment
        fields = ['assignment__name',]