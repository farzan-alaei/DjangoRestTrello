from django.urls import path
from workspaces.views import (
    WorkspacesList,
    WorkspaceDetail,
    WorkspacesMemberList,
    WorkspacesMembershipDetail,
)

urlpatterns = [
    path("", WorkspacesList.as_view()),
    path("<uuid:id>/", WorkspaceDetail.as_view()),
    path("<uuid:id>/members/", WorkspacesMemberList.as_view()),
    path("members/<uuid:id>/", WorkspacesMembershipDetail.as_view()),
]
