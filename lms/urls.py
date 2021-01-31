# Core Django imports.
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include

# LMS app imports
from lms.views.account.login_view import UserLoginView
from lms.views.account.logout_view import UserLogoutView
from lms.views.account.register_view import (
    ActivateView,
    AccountActivationSentView,
    UserRegisterView,
)
from lms.views.account.subscriber_view import subscribe, subscribe_confirm, subscribe_delete, sub_delete
from lms.views.assignment.assignment_views import (
    AssignmentHomeView,
    AssignmentDetailView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentDeleteView,
    CommentCreateView, AssignmentHomeStudentView, AssignmentDetailStudentView,
)
from lms.views.blog.blog_view import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from lms.views.course.course_publish_views import (
    CoursePublishView,
    CourseUnPublishView
)
from lms.views.course.course_registration_views import (
    CourseRegistrationView,
)
from lms.views.course.course_views import (
    CourseListView,
    GradeBookCourseView,
    StudentGradeBookCourseView, CourseCreateView
    # table_download
)
from lms.views.course.grading_scheme_view import (
    GradingSchemeUpdateView,
    GradingSchemeCreateView
)
from lms.views.course.group_creation_view import (
    GroupCreationRequestView,
    GroupCreationRequestSentView,
    ViewGroupsView
)
from lms.views.course.mail_to_admin_view import (
    MailToAdminView

)
from lms.views.course.settings_view import (
    CourseDetailsView,
    CourseManageView,
    CourseSectionsView,
    CourseStatisticsView
)
from lms.views.dashboard.dashboard_views import (
    DashboardHomeView,
    DashboardProfileView,
    dashboard_list,
    dashboard_details,
    dashboard_subscribe
)
from lms.views.notification.notification_settings_view import (
    NotificationSettingsView,
)
from lms.views.quiz.quiz_views import (
    compute_stats,
    fetch_questions_one_at_a_time,
    fetch_questions,
    quiz_home,
    quiz_detail,
    preview_quiz,
    enter_quiz_comment,
    quiz_publish, QuizCreateView, QuizUpdateView, QuizDeleteView,
    QuizQuestionCreateView, QuizQuestionUpdateView, QuizQuestionDeleteView
)

# Specifies the app name for name spacing.
app_name = "lms"

# lms/urls.py
urlpatterns = [

    # LMS URLS #

    # /home/
    path(
        route='course/<int:pk>/',
        view=CourseListView.as_view(),
        name='course-home'
    ),

    # /home/
    path(
        route='course/',
        view=CourseListView.as_view(),
        name='course-home'
    ),

    # Blog URLS #

    # /home/blog
    path(
        route='blog/',
        view=PostListView.as_view(),
        name='blog-home'
    ),

    path(
        route='blog/user/<str:username>/',
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

    # /
    path('', dashboard_list, name='home'),
    path('<int:page>', dashboard_list, name='home'),
    path('coursedetails/<int:pk>/', dashboard_details),
    path('subscribe/<int:pk>/', dashboard_subscribe),

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

    # /author/course/register
    path(
        route="course/register/<int:pk>/",
        view=CourseRegistrationView.as_view(),
        name="course_register"
    ),

    # /author/course/publish
    path(
        route="course/publish/<int:pk>/",
        view=CoursePublishView.as_view(),
        name="course_publish"
    ),

    # /author/course/unpublish
    path(
        route="course/unpublish/<int:pk>/",
        view=CourseUnPublishView.as_view(),
        name="course_unpublish"
    ),

    path(
        route="course/create/",
        view=CourseCreateView.as_view(),
        name="course_create"
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
        route="course/<int:pk>/grading_scheme/new/",
        view=GradingSchemeCreateView.as_view(),
        name="course_grading_scheme_create"
    ),
    path(
        route="course/<int:pk>/grading_scheme/update/",
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
        route="course/<int:pk>/view_groups/",
        view=ViewGroupsView.as_view(),
        name="view_groups"
    ),

    # COURSE STUDENT -  Mail To Admin
    path(
        route="course/<int:pk>/mail_to_admin/",
        view=MailToAdminView.as_view(),
        name="mail_to_admin"
    ),

    # COURSE GRADEBOOK - Teacher's View
    path(
        route="course/<int:course_id>/grades/",
        view=GradeBookCourseView.as_view(),
        name='gradebook-course'
    ),

    path(
        route="course/<int:course_id>/student_grades/",
        view=StudentGradeBookCourseView.as_view(),
        name='gradebook-course-student'
    ),

    # By Quiz Teacher View Team.[Start]
    path('course/<int:course_id>/quiz/course_stats/', compute_stats, name="compute_stats"),

    path('course/<int:course_id>/quiz/<int:pk>/one_at_a_time/', fetch_questions_one_at_a_time,
         name="fetch_questions_one_at_a_time"),

    path('course/<int:course_id>/quiz/<int:pk>/fetch_questions/', fetch_questions, name="fetch_questions"),

    path('course/<int:course_id>/quiz/home/', quiz_home, name="quiz_home"),

    path('course/<int:course_id>/quiz/create/', QuizCreateView.as_view(), name="quiz_create"),
    path('course/<int:course_id>/quiz/<int:pk>/update/', QuizUpdateView.as_view(), name="quiz_update"),
    path('course/<int:course_id>/quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name="quiz_delete"),

    path('course/<int:course_id>/quiz/<int:quiz_id>/question/create', QuizQuestionCreateView.as_view(),
         name="quiz_question_create"),
    path('course/<int:course_id>/quiz/<int:quiz_id>/question/<int:pk>/update/', QuizQuestionUpdateView.as_view(),
         name="quiz_question_update"),
    path('course/<int:course_id>/quiz/<int:quiz_id>/question/<int:pk>/delete/', QuizQuestionDeleteView.as_view(),
         name="quiz_question_delete"),

    path('course/<int:course_id>/quiz/<int:pk>/detail/', quiz_detail, name="quiz_view"),

    path('course/<int:course_id>/quiz/<int:pk>/preview/', preview_quiz, name="preview_quiz"),

    path('course/<int:course_id>/quiz/<int:pk>/enter_quiz_comment/', enter_quiz_comment, name="enter_quiz_comment"),

    path('course/<int:course_id>/quiz/<int:pk>/publish/', quiz_publish, name='quiz_publish'),
    # By Quiz Teacher View Team.[End]

    # Assignment Views
    path(
        route="course/<int:pkcourse>/student_assignment/home/",
        view=AssignmentHomeStudentView.as_view(),
        name="assignment_student_home"
    ),

    path(
        route="course/<int:pkcourse>/student_assignment/home/<int:pk>/",
        view=AssignmentDetailStudentView.as_view(),
        name="assignment_student_detail"
    ),

    path(
        route="course/<int:pkcourse>/assignment/home/",
        view=AssignmentHomeView.as_view(),
        name="assignment_home"
    ),

    path(
        route="course/<int:pkcourse>/assignment/home/<int:pk>/",
        view=AssignmentDetailView.as_view(),
        name="assignment_detail"
    ),

    path(
        route="course/<int:pkcourse>/assignment/create/",
        view=AssignmentCreateView.as_view(),
        name="assignment_create"
    ),
    path(
        route='course/<int:pkcourse>/assignment/<int:pk>/update/',
        view=AssignmentUpdateView.as_view(),
        name='assignments_update'
    ),

    path(
        route='course/<int:pkcourse>/assignment/<int:pk>/delete/',
        view=AssignmentDeleteView.as_view(),
        name='assignment_delete'),

    path(
        route="course/<int:pkcourse>/assignment/<int:pk>/comment/",
        view=CommentCreateView.as_view(),
        name="comment_create"
    ),

    path(route='account/subscribe', view=subscribe, name='subscribe'),
    path(route='account/subscribe_confirm', view=subscribe_confirm, name='subscribe_confirm'),
    path(route='account/subscribe_delete', view=subscribe_delete, name='subscribe_delete'),
    path(route='account/sub_delete', view=sub_delete, name='sub_delete'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
