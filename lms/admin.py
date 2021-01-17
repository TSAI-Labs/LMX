from django.contrib import admin

# LMS application imports.
from .models.course_model import Course, GradingSchemeName, Section, GradingScheme
from .models.enrollment_model import Enrollment
from .models.users_model import Staff, Student


# Registers the student profile model at the admin backend.
class StudentAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user__username',)
    ordering = ['user__username', ]


admin.site.register(Student, StudentAdmin)


# Registers the staff profile model at the admin backend.
class StaffAdmin(admin.ModelAdmin):
    list_filter = ('is_admin', 'is_teacher', 'is_teaching_assistant')
    search_fields = ('user__username',)
    ordering = ['user__username', 'is_admin', 'is_teacher', 'is_teaching_assistant']


admin.site.register(Staff, StaffAdmin)


# Registers the course details model at the admin backend.
class CourseAdmin(admin.ModelAdmin):
    list_filter = ('allow_self_enroll', 'enrollment_open_to_all', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ['title', 'start_date']


admin.site.register(Course, CourseAdmin)


# Registers enrollment model at the admin backend.
class EnrollmentAdmin(admin.ModelAdmin):
    list_filter = ('course', 'section', 'student')
    search_fields = ('student__user__username', 'course__title')
    ordering = ['course__title', 'student__user__username']


admin.site.register(Enrollment, EnrollmentAdmin)


# Registers the course-section model at the admin backend.
class SectionAdmin(admin.ModelAdmin):
    list_filter = ('section_name', 'course')
    search_fields = ('section_name', 'course')
    ordering = ['section_name', 'course']


admin.site.register(Section, SectionAdmin)


# Registers the grading scheme name model at the admin backend.
class GradingSchemeNameAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ['name']


admin.site.register(GradingSchemeName, GradingSchemeNameAdmin)


# Registers the grading scheme model at the admin backend.
class GradingSchemeAdmin(admin.ModelAdmin):
    list_filter = ('scheme_name',)
    search_fields = ('scheme_name__name', 'grade')
    ordering = ['scheme_name__name', '-score_range_begin']


admin.site.register(GradingScheme, GradingSchemeAdmin)
