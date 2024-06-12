from rest_framework import serializers
from workspaces.models import WorkspacesMembership, Workspace
from accounts.serializers import UserSerializer


class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    member = UserSerializer(many=True)

    class Meta:
        model = Workspace
        fields = ("id", "owner", "title", "description", "member")
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
    class Meta:
        model = WorkspacesMembership
        fields = "__all__"
