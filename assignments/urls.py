# Core Django imports.
from django.urls import path

from assignments.views import (
    AssignmentHomeView,
    AssignmentDetailView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentDeleteView
)

# Specifies the app name for name spacing.
app_name = "assignments"

# lms/urls.py
urlpatterns = [

    
    path(
        route="assignment/home",
        view=AssignmentHomeView.as_view(),
        name="assignment_home"
    ),

    
    path(
        route="user/assignment/home/<int:pk>",
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
        name='assignments_update'
    ),

    path(
        route='assignment/<int:pk>/delete/',
        view=AssignmentDeleteView.as_view(),
        name='assignment_delete'),

    ]