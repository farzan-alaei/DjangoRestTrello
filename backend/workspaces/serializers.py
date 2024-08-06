from rest_framework import serializers

from accounts.serializers import UserSerializer
from workspaces.models import WorkspacesMembership, Workspace


class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for membership.
    """
    member = UserSerializer(read_only=True)

    class Meta:
        model = WorkspacesMembership
        fields = ("member", "access_level")


class WorkspaceSerializer(serializers.ModelSerializer):
    """
    Serializer for workspace.
    """
    owner = UserSerializer(read_only=True)
    membership = MembershipSerializer(
        source="membership_set", many=True, read_only=True
    )

    class Meta:
        model = Workspace
        fields = ("id", "owner", "title", "description", "membership")
        read_only_fields = ("owner",)
        ref_name = "WorkspaceSerializer"

    def create(self, validated_data):
        """
        Creates a new workspace with the given data.
        """
        workspace = Workspace.objects.create(**validated_data)
        return workspace

    def get_membership(self, user, workspace):
        """
        Get membership for given user and workspace.
        """
        try:
            return WorkspacesMembership.objects.get(member=user, workspace=workspace)
        except WorkspacesMembership.DoesNotExist:
            return None

    def get_boards(self, obj):
        """
        Get list of board names for given workspace.
        """
        return [board.name for board in obj.get_boards()]


class WorkspacesMembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for workspaces membership.
    """
    workspace = serializers.StringRelatedField(read_only=True)
    member = UserSerializer(read_only=True)

    class Meta:
        model = WorkspacesMembership
        fields = ("id", "workspace", "member", "access_level")
