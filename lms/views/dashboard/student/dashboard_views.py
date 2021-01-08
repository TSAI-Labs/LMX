# Django imports.
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View

from lms.models.course_model import Course
from lms.models.assignment_model import Assignment
from lms.views.account.login_view import UserLoginView


class DashboardHomeView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'dashboard/student/dashboard_home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            assignt = Assignment.objects.all()
            print(assignt)
            print(list(filter(lambda x: x.available_until > now(), assignt)))
            courses = Course.objects.filter(student=request.user)
            self.context.update(published_courses=list(filter(lambda x: x.published, courses)))
            self.context.update(unpublished_courses=list(filter(lambda x: not x.published, courses)))
            self.context.update(assignments=list(filter(lambda x: x.available_until > now(), assignt)))
            self.context.update(is_profile_view=False)
            return render(request, self.template_name, self.context)
        else:
            return redirect(UserLoginView.as_view())


# TODO: Dummy part
class ProfileView(LoginRequiredMixin, View):
    """
    Display user profile (dummy).
    """
    context = {}
    template_name = 'dashboard/student/dummy_profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile = User.objects.get(username__iexact=request.user)
            self.context.update(user_profile=user_profile)
            self.context.update(is_profile_view=True)
            print(user_profile.username)
            return render(request, self.template_name, self.context)
        else:
            return redirect(UserLoginView.as_view())
