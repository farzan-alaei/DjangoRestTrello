from rest_framework import serializers

from accounts.serializers import UserSerializer
from workspaces.models import WorkspacesMembership, Workspace


class MembershipSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    class Meta:
        model = WorkspacesMembership
        fields = ("member", "access_level")


class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    membership = MembershipSerializer(
        source="membership_set", many=True, read_only=True
    )

    class Meta:
        model = Workspace
        fields = ("id", "owner", "title", "description", "membership")
        read_only_fields = ("owner",)

    def create(self, validated_data):
        workspace = Workspace.objects.create(**validated_data)
        return workspace

    def get_membership(self, user, workspace):
        try:
            return WorkspacesMembership.objects.get(member=user, workspace=workspace)
        except WorkspacesMembership.DoesNotExist:
            return None

    def get_boards(self, obj):
        return [board.name for board in obj.get_boards()]


class WorkspacesMembershipSerializer(serializers.ModelSerializer):
    workspace = serializers.StringRelatedField(read_only=True)
    member = UserSerializer(read_only=True)

    class Meta:
        model = WorkspacesMembership
        fields = ("id", "workspace", "member", "access_level")
