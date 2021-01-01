# Core Django imports.
from django.urls import path

# LMS app imports

from lms.views.course.course_views import (
    CourseListView,
)

from lms.views.dashboard.student.dashboard_views import (
    DashboardHomeView,
)

from lms.views.account.register_view import \
    (
      ActivateView,
      AccountActivationSentView,
      UserRegisterView,
    )

from lms.views.assignment.teacher.assignment_views import (
    AssignmentListView,
    AssignmentDetailView,
    AssignmentCreateView
)

from lms.views.account.logout_view import UserLogoutView
from lms.views.account.login_view import UserLoginView

# Specifies the app name for name spacing.
app_name = "lms"

# lms/urls.py
urlpatterns = [

    # LMS URLS #

    # /home/
    path(
        route='',
        view=CourseListView.as_view(),
        name='home'
    ),

    # ACCOUNT URLS #

    # /account/login/
    path(
        route='account/login/',
        view=UserLoginView.as_view(),
        name='login'
    ),

    # /account/login/
    path(
        route='account/register/',
        view=UserRegisterView.as_view(),
        name='register'
    ),

    # /account/logout/
    path(
        route='account/logout/',
        view=UserLogoutView.as_view(),
        name='logout'
    ),

    path(route='account_activation_sent/',
         view=AccountActivationSentView.as_view(),
         name='account_activation_sent'
         ),

    path(route='activate/<uidb64>/<token>/',
         view=ActivateView.as_view(),
         name='activate'
         ),

    # DASHBOARD URLS #

    # /author/dashboard/home/
    path(
        route="student/dashboard/home/",
        view=DashboardHomeView.as_view(),
        name="dashboard_home"
    ),

        path(
        route="author/assignment/home",
        view=AssignmentListView.as_view(),
        name="assignment_home"
    ),

    path(
        route="author/assignment/home/<int:pk>",
        view=AssignmentDetailView.as_view(),
        name="assignment_detail"
    ),

    path(
        route="author/assignment/create",
        view=AssignmentCreateView.as_view(),
        name="assignment_create"
    ),

]

