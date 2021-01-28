# Core Django imports.
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# LMS app imports
from lms.views.account.login_view import UserLoginView
from lms.views.account.logout_view import UserLogoutView
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
from lms.views.course.course_views import (
    CourseListView,
    GradeBookCourseView
    # table_download
)
from lms.views.course.grading_scheme_view import (
    GradingSchemeUpdateView,
    GradingSchemeCreateView
)
from lms.views.course.settings_view import (
    CourseDetailsView,
    CourseManageView,
    CourseSectionsView,
    CourseStatisticsView
)

from lms.views.course.mail_to_admin_view import (
    MailToAdminView
    
)

from lms.views.course.group_creation_view import (
    GroupCreationRequestView,
    GroupCreationRequestSentView,
    ViewGroupsView
)

from lms.views.dashboard.dashboard_views import (
    DashboardHomeView,
    DashboardProfileView,
)
from lms.views.notification.notification_settings_view import (
    NotificationSettingsView,
)

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
    ),

    # COURSE SETTINGS URLS #

    path(
        route="course/<int:pk>/details/",
        view=CourseDetailsView.as_view(),
        name="course_details"
    ),
    path(
        route="course/<int:pk>/manage/",
        view=CourseManageView.as_view(),
        name="course_manage"
    ),
    path(
        route="course/<int:pk>/sections/",
        view=CourseSectionsView.as_view(),
        name="course_sections"
    ),
    path(
        route="course/<int:pk>/statistics/",
        view=CourseStatisticsView.as_view(),
        name="course_statistics"
    ),
    path(
        route="course/<int:pk>/grading_scheme/new",
        view=GradingSchemeCreateView.as_view(),
        name="course_grading_scheme_create"
    ),
    path(
        route="course/<int:pk>/grading_scheme/update",
        view=GradingSchemeUpdateView.as_view(),
        name="course_grading_scheme_update"
    ),

    # COURSE STUDENT - Group CREATION REQUEST
    path(
        route="course/<int:pk>/group_creation_request/",
        view=GroupCreationRequestView.as_view(),
        name="group_creation_request"
    ),
    path(route='group_request/<int:ck>/<uidb64>/<token>/',
         view=GroupCreationRequestSentView.as_view(),
         name='group_request'
    ),

    # View GROUPS -  
    path(
        route="course/<int:pk>/view_groups",
        view=ViewGroupsView.as_view(),
        name="view_groups"
    ),

    # COURSE STUDENT -  Mail To Admin 
    path(
        route="course/<int:pk>/mail_to_admin",
        view=MailToAdminView.as_view(),
        name="mail_to_admin"
    ),

    # COURSE GRADEBOOK - Teacher's View
    path(
        route="course/grades",
        view=GradeBookCourseView.as_view(),
        name='gradebook-course'
    )

    # path to download csv file
    # path('_export=csv', table_download),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
