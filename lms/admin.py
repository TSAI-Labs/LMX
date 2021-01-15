from django.contrib import admin
from django.contrib import messages

# LMS application imports.
from .models.student_model import Profile
from .models.course_model import Course, StudentCourse
from .models.assignment_model import Assignment
from .models.users_model import Role
from .models.files_model import File
from .models.blog_model import Post
from .models.notification_settings_model import NotificationSetting

class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    ordering = ['user', ]

# Registers the notification setting model for user at the admin backend.
admin.site.register(NotificationSetting, NotificationSettingAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', 'email_confirmed')
    search_fields = ('user','user_tz')
    ordering = ['user', ]

# Registers the student profile model at the admin backend.
admin.site.register(Profile, ProfileAdmin)

class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'courses', 'registered')
    list_filter = ('user',)
    search_fields = ('user__username', 'courses')
    ordering = ['user__username', ]

# Registers the student courses model at the admin backend.
admin.site.register(StudentCourse, StudentCourseAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin', 'is_teacher', 'is_teaching_assistant', 'is_student')
    list_filter = ('is_admin', 'is_teacher', 'is_teaching_assistant', 'is_student')
    search_fields = ('user__username',)
    ordering = ['user__username',]

# Registers the staff profile model at the admin backend.
admin.site.register(Role, RoleAdmin)

class CourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'published')
    list_filter = ('user',)
    search_fields = ('title',)

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

class PostAdmin(admin.ModelAdmin):

    list_display = ('author', 'title', 'date_posted')
    list_filter = ('author','date_posted')
    search_fields = ('author','date_posted')

# Registers the Blog Post model at the admin backend.
admin.site.register(Post, PostAdmin)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass
