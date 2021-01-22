from django.contrib import admin

# Register your models here.
from .models.assignment_model import Assignment, Comment

# class AssignmentAdmin(admin.ModelAdmin):
#     list_filter = ('user',)
#     search_fields = ('user',)
#     ordering = ['user', ]

# Registers the Assignment model at the admin backend.
admin.site.register(Assignment)

# Registers the Assignment model at the admin backend.
admin.site.register(Comment)