from django.contrib import admin

# LMS application imports.
from .models.student_model import Profile
from .models.course_model import Course


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ['user', ]


# Registers the student profile model at the admin backend.
admin.site.register(Profile, ProfileAdmin)


class CourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'student',)
    list_filter = ('student',)
    search_fields = ('title',)
    raw_id_fields = ('student',)


# Registers the article model at the admin backend.
admin.site.register(Course, CourseAdmin)

from .models.dummy_model import DummyAssignment, DummyStudent
class DummyStudentAdmin(admin.ModelAdmin):
    
    list_filter = ('name', 'email',)
    search_fields = ('name', 'email',)
    ordering = ['name',]

admin.site.register(DummyStudent, DummyStudentAdmin)

class DummyAssignmentAdmin(admin.ModelAdmin):
    
    list_display = ('student', 'title', 'grade',
                    'alloted_mark', 'max_mark')
    
    list_filter = ('student', 'title', 'grade',
                   'alloted_mark')
    
    search_fields = ('title', 'grade',
                   'alloted_mark')
    
    raw_id_fields = ('student', )

admin.site.register(DummyAssignment, DummyAssignmentAdmin)