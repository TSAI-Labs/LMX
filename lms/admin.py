from django.contrib import admin

# LMS application imports.
from .models.student_model import Profile
from .models.course_model import Course
from .models.assignment_model import Assignment


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


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass
