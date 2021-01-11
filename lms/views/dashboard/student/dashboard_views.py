# Django imports.
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View

from lms.models.course_model import Course
from lms.models.assignment_model import Assignment
from lms.views.account.login_view import UserLoginView

from lms.forms.account.register_form import UserUpdateForm
from lms.forms.dashboard.profile_form import ProfileUpdateForm


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

class DashboardProfileView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    # context = {}
    # template_name = 'dashboard/student/dashboard_profile.html'

    def get(self, request, *args, **kwargs):

        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect('lms:dashboard_profile')

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'is_profile_view':True
        }

        template_name = 'dashboard/student/profile.html'

        return render(request, template_name, context)
