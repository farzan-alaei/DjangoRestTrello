from rest_framework import permissions
from workspaces.models import WorkspacesMembership, Workspace


class BaseWorkspacePermission(permissions.BasePermission):
    def get_membership(self, user, workspace):
        if not user.is_authenticated:
            return None
        try:
            return WorkspacesMembership.objects.get(member=user, workspace=workspace)
        except WorkspacesMembership.DoesNotExist:
            return None


class IsWorkspaceAdminOrMemberReadOnly(BaseWorkspacePermission):
    def has_object_permission(self, request, view, obj):
        membership = self.get_membership(request.user, obj)
        if request.user == obj.owner:
            return True

        if not membership:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return membership.access_level == WorkspacesMembership.AccessLevel.ADMIN


class IsWorkspaceMember(BaseWorkspacePermission):
    def has_object_permission(self, request, view, obj):
        membership = self.get_membership(request.user, obj)
        return membership
