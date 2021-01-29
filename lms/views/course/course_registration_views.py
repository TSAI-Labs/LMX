# Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import View

from lms.models.course_model import Course, StudentCourse


class CourseRegistrationView(LoginRequiredMixin, View):
    """
    Register course of the dashboard.
    """

    def post(self, request, *args, **kwargs):
        selected_course = Course.objects.get(id=kwargs['pk'])
        try:
            obj = StudentCourse.objects.get(user=request.user, courses=selected_course)
            setattr(obj, 'registered', True)
            obj.save()
        except StudentCourse.DoesNotExist:
            obj = StudentCourse(user=request.user, courses=selected_course, registered=True)
            obj.save()

        return redirect('lms:dashboard_home')
