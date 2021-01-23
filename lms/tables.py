# lms/tables.py
import django_tables2 as tables
from lms.models.assignment_model import StudentAssignment

class StudentAssignmentTable(tables.Table):
    class Meta:
        model = StudentAssignment
        template_name = "django_tables2/bootstrap4.html"
        
        fields = ('user', 'assignment__name', 'assignment__max_grade')

import django_filters

class StudentAssignmentFilter(django_filters.FilterSet):
    class Meta:
        model = StudentAssignment
        fields = ['user']
