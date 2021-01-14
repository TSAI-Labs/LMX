# Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from lms.forms.account.register_form import UserUpdateForm
from lms.forms.dashboard.profile_form import ProfileUpdateForm

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
            'p_form': p_form
        }

        template_name = 'dashboard/student/profile.html'

        return render(request, template_name, context)