from django.contrib import admin
from django.contrib import messages

# LMS application imports.
from .models.student_model import Profile
from .models.course_model import Course
from .models.users_model import Staff, Student
from .models.files_model import File


class StudentAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user__username',)
    ordering = ['user__username', ]


# Registers the student profile model at the admin backend.
admin.site.register(Student, StudentAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_filter = ('is_admin', 'is_teacher', 'is_teaching_assistant')
    search_fields = ('user__username',)
    ordering = ['user__username', 'is_admin', 'is_teacher', 'is_teaching_assistant']


# Registers the staff profile model at the admin backend.
admin.site.register(Staff, StaffAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ['user', ]


# Registers the student profile model at the admin backend.
admin.site.register(Profile, ProfileAdmin)


class CourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'published') #('title', 'student', 'published')
    # list_filter = ('student',)
    search_fields = ('title',)
    # raw_id_fields = ('student',)

    def publish_course(modeladmin, request, queryset): 
        queryset.update(published = 1) 
        messages.success(request, "Selected courses are published successfully !!") 
  
    def unpublish_course(modeladmin, request, queryset): 
        queryset.update(published = 0) 
        messages.success(request, "Selected courses are unpublished successfully !!") 
  
    admin.site.add_action(publish_course, "Publish Course") 
    admin.site.add_action(unpublish_course, "Unpublish Course")


# Registers the article model at the admin backend.
admin.site.register(Course, CourseAdmin)


class FileAdmin(admin.ModelAdmin):

    list_display = ('name', 'date_created',)
    list_filter = ('name',)
    search_fields = ('name',)
    raw_id_fields = ('course',)


# Registers the article model at the admin backend.
admin.site.register(File, FileAdmin)