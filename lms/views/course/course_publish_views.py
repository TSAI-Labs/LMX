# Django imports.
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from lms.models.course_model import Course, StudentCourse
from lms.models.user_role_model import Role
from lms.views.account.login_view import UserLoginView


class CoursePublishView(LoginRequiredMixin, View):
    """
    Publish course of the dashboard.
    """

    def post(self, request, *args, **kwargs):
        selected_course = Course.objects.get(id=kwargs['pk'])
        selected_course.published=True
        selected_course.save()
        return redirect('lms:dashboard_home')

class CourseUnPublishView(LoginRequiredMixin, View):
    """
    Unpublish course of the dashboard.
    """

    def post(self, request, *args, **kwargs):
        selected_course = Course.objects.get(id=kwargs['pk'])
        selected_course.published=False
        selected_course.save()
        return redirect('lms:dashboard_home')
