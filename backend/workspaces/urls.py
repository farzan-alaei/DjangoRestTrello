from django.urls import path
from workspaces.views import (
    WorkspacesList,
    WorkspaceDetail,
    WorkspacesMemberList,
    WorkspacesMembershipDetail,
)

urlpatterns = [
    path("", WorkspacesList.as_view(), name="workspaces-list"),
    path("<uuid:id>/", WorkspaceDetail.as_view(), name="workspace-detail"),
    path("<uuid:id>/members/", WorkspacesMemberList.as_view(), name="workspace_members"),
    path("members/<uuid:id>/", WorkspacesMembershipDetail.as_view(), name="workspace_membership"),
]
