# Django imports.
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from lms.forms.notification.notification_settings_form import NotificationSettingUpdateForm
#TODO Auto object generation
class NotificationSettingsView(LoginRequiredMixin, View):
    """
    Display notification settings of the user.
    """

    def get(self, request, *args, **kwargs):

        u_form = NotificationSettingUpdateForm(instance=request.user.notificationsetting)
        context = {
            'u_form': u_form
        }

        template_name = 'notification/student/notification_settings.html'

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):

        u_form = NotificationSettingUpdateForm(request.POST, instance=request.user.notificationsetting)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Notification Settings has been updated!')
            return redirect('lms:notification_settings')
        else:
            messages.error(request, f'Check Selected Settings')

        context = {
            'u_form': u_form
        }

        template_name = 'notification/student/notification_settings.html'

        return render(request, template_name, context)
