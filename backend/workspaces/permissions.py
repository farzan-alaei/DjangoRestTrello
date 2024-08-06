from rest_framework import permissions

from workspaces.models import WorkspacesMembership


class BaseWorkspacePermission(permissions.BasePermission):
    """
    Base permission class for workspaces.
    """
    def get_membership(self, user, workspace):
        """
        Get membership of a user with a workspace.
        """
        if not user.is_authenticated:
            return None
        try:
            return WorkspacesMembership.objects.get(member=user, workspace=workspace)
        except WorkspacesMembership.DoesNotExist:
            return None


class IsWorkspaceAdminOrMemberReadOnly(BaseWorkspacePermission):
    """
    Check if the user is a member of the workspace or the owner of the workspace.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a member of the workspace or the owner of the workspace.
        Returns True if the user is the owner of the workspace or the user is a member
        of the workspace with an admin access level and the HTTP method is safe.
        """
        membership = self.get_membership(request.user, obj)
        if request.user == obj.owner:
            return True

        if not membership:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return membership.access_level == WorkspacesMembership.AccessLevel.ADMIN


class IsWorkspaceMember(BaseWorkspacePermission):
    """
    Check if the user is a member of the workspace.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a member of the workspace.
        """
        membership = self.get_membership(request.user, obj)
        return membership
