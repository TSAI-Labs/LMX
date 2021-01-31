from django.contrib import admin
from django.contrib import messages

# LMS application imports.
from .models.assignment_model import Assignment, StudentAssignment
from .models.blog_model import Post
from .models.course_model import Course, StudentCourse, GradingSchemeName, Section, GradingScheme, Group
from .models.files_model import File
from .models.notification_settings_model import NotificationSetting
from .models.profile_model import Profile
from .models.quiz_model import Quiz, Responses, Question
from .models.subscriber_model import Subscriber, Newsletter
from .models.user_role_model import Role


class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    ordering = ['user', ]


# Registers the notification setting model for user at the admin backend.
admin.site.register(NotificationSetting, NotificationSettingAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', 'email_confirmed')
    search_fields = ('user', 'user_tz')
    ordering = ['user', ]


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
    ordering = ['user__username', ]


# Registers the staff profile model at the admin backend.
admin.site.register(Role, RoleAdmin)


# Registers the course details model at the admin backend.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'published')
    list_filter = ('user',)
    search_fields = ('title',)
    ordering = ['title', 'start_date']

    def publish_course(modeladmin, request, queryset):
        queryset.update(published=1)
        messages.success(request, "Selected courses are published successfully !!")

    def unpublish_course(modeladmin, request, queryset):
        queryset.update(published=0)
        messages.success(request, "Selected courses are unpublished successfully !!")

    admin.site.add_action(publish_course, "Publish Course")
    admin.site.add_action(unpublish_course, "Unpublish Course")


# Registers the article model at the admin backend.
admin.site.register(Course, CourseAdmin)


# Registers the course-section model at the admin backend.
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'course')
    list_filter = ('section_name', 'course')
    search_fields = ('section_name', 'course')
    ordering = ['section_name', 'course']


admin.site.register(Section, SectionAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'course')
    list_filter = ('group_name', 'course')
    search_fields = ('group_name', 'course')
    ordering = ['group_name', 'course']


admin.site.register(Group, GroupAdmin)


# Registers the grading scheme name model at the admin backend.
class GradingSchemeNameAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ['name']


admin.site.register(GradingSchemeName, GradingSchemeNameAdmin)


# Registers the grading scheme model at the admin backend.
class GradingSchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_name', 'grade', 'score_range_begin', 'score_range_end')
    list_filter = ('scheme_name',)
    search_fields = ('scheme_name__name', 'grade')
    ordering = ['scheme_name__name', '-score_range_begin']


admin.site.register(GradingScheme, GradingSchemeAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created',)
    list_filter = ('name',)
    search_fields = ('name',)
    raw_id_fields = ('course',)


# Registers the article model at the admin backend.
admin.site.register(File, FileAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'date_posted')
    list_filter = ('author', 'date_posted')
    search_fields = ('author', 'date_posted')


# Registers the Blog Post model at the admin backend.
admin.site.register(Post, PostAdmin)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'for_course', 'created_by')
    list_filter = ('for_course', 'created_by')


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'assignment',)
    list_filter = ('user__username', 'assignment__name',)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_filter = ('email',)
    search_fields = ('email',)
    ordering = ['email', ]


admin.site.register(Subscriber, SubscriberAdmin)


# def send_newsletter(modeladmin, request, queryset):
#     for newsletter in queryset:
#         newsletter.send(request)
# send_newsletter.short_description = "Send selected Newsletters to all subscribers"
#
# class NewsletterAdmin(admin.ModelAdmin):
#     actions = [send_newsletter]
# admin.site.register(Newsletter, NewsletterAdmin)

# By Quiz Teacher View Team [Start]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'questiontype', 'quiz',)
    list_filter = ('questiontype', 'quiz',)
    search_fields = ('questiontype', 'quiz',)
    ordering = ['quiz', ]


admin.site.register(Question, QuestionAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('Quizname', 'course', 'created_by',)
    list_filter = ('Quizname', 'course', 'created_by',)
    search_fields = ('Quizname', 'course', 'created_by',)
    ordering = ['course', 'Quizname']


admin.site.register(Quiz, QuizAdmin)


admin.site.register(Responses)
# By Quiz Teacher View Team [Finish]
