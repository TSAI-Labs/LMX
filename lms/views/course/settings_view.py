# Core Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

# Blog application imports.
from lms.models.course_model import Course
from lms.models.users_model import Staff


class CourseDetailsView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Class View to show / update the course_details for staff
    """

    model = Course
    fields = ['title', 'thumbnail', 'time_zone', 'start_date', 'end_date', 'grading_scheme', 'description',
              'allow_self_enroll', 'enrollment_open_to_all']
    template_name = "lms/course/settings/course_details_tab.html"
    success_message = 'Course details have been successfully updated!'

    # url to redirect to on success
    def get_success_url(self, **kwargs):
        return reverse('lms:course_details', kwargs={'pk': self.object.pk})

    # Restrict access to only staff members
    def test_func(self):
        return len(Staff.objects.all().filter(user=self.request.user)) == 1


# todo: full implementation
class CourseSectionsView(ListView):
    model = Course
    template_name = "lms/course/settings/sections_tab.html"


# todo: full implementation
class CourseSettingsView(ListView):
    model = Course
    template_name = "lms/course/settings/settings_tab.html"


# todo: full implementation
class CourseStatisticsView(ListView):
    model = Course
    template_name = "lms/course/settings/statistics_tab.html"
