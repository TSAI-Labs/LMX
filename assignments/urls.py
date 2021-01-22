# Core Django imports.
from django.urls import path, include, re_path

from assignments.views import (
    AssignmentBaseView,
    AssignmentListView,
    AssignmentDetailView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentDeleteView,
    CommentCreateView
)

# Specifies the app name for name spacing.
app_name = "assignments"

# lms/urls.py
urlpatterns = [
    path(
        route="assignment/home",
        view=AssignmentBaseView.as_view(),
        name="assignment_home"
    ),

    path(
        route="assignment/Lists",
        view=AssignmentListView.as_view(),
        name="assignment_list"
    ),

    path(
        route="assignment/Detail/<int:pk>",
        view=AssignmentDetailView.as_view(),
        name="assignment_detail"
    ),

    path(
        route="assignment/create",
        view=AssignmentCreateView.as_view(),
        name="assignment_create"
    ),
    path(
        route='assignment/<int:pk>/update/',
        view=AssignmentUpdateView.as_view(),
        name='assignment_update'
    ),

    path(
        route='assignment/<int:pk>/delete/',
        view=AssignmentDeleteView.as_view(),
        name='assignment_delete'),

    path(
        route="assignment/<int:pk>/comment/",
        view=CommentCreateView.as_view(),
        name="comment_create"
    ),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls'))

    ]