# Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View



class DashboardHomeView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'dashboard/student/dashboard_home.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.context)
