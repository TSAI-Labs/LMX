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


class CourseRegistraionView(LoginRequiredMixin, View):
    """
    Register course of the dashboard.
    """

    def post(self, request, *args, **kwargs):
        selected_course = Course.objects.get(id=kwargs['pk'])
        studentcourse = StudentCourse(user=request.user, courses=selected_course, registered=True)
        studentcourse.save()
        return redirect('lms:dashboard_home')
