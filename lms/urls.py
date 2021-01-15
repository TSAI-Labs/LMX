# Core Django imports.
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


# LMS app imports

from lms.views.course.course_views import (
    CourseListView,
)

from lms.views.dashboard.student.dashboard_views import (
    DashboardHomeView,
    DashboardProfileView,
)

from lms.views.notification.notification_settings_view import (
    NotificationSettingsView,
)

from lms.views.account.register_view import \
    (
      ActivateView,
      AccountActivationSentView,
      UserRegisterView,
    )

from lms.views.blog.blog_view import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
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

    # Blog URLS #
    # /home/blog
    path(
        route='blog/',
        view=PostListView.as_view(),
        name='blog-home'
        ),

    path(
        route='blog/user/<str:username>',
        view=UserPostListView.as_view(),
        name='user-posts'
        ),

    path(
        route='blog/post/<int:pk>/',
        view=PostDetailView.as_view(),
        name='post-detail'
        ),

    path(
        route='blog/post/new/',
        view=PostCreateView.as_view(),
        name='post-create'
        ),

    path(
        route='blog/post/<int:pk>/update/',
        view=PostUpdateView.as_view(),
        name='post-update'
        ),

    path(
        route='blog/post/<int:pk>/delete/',
        view=PostDeleteView.as_view(),
        name='post-delete'
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
        route="dashboard/home/",
        view=DashboardHomeView.as_view(),
        name="dashboard_home"
    ),

    # /author/dashboard/profile/
    path(
        route="dashboard/profile/",
        view=DashboardProfileView.as_view(),
        name="dashboard_profile"
    ),

    # /author/notification/
    path(
        route="notifications/",
        view=NotificationSettingsView.as_view(),
        name="notification_settings"
    )

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
