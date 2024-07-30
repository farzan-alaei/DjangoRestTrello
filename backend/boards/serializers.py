from rest_framework import serializers

from workspaces.models import Workspace
from .models import Board, List, Task, Comment, Label


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "title"]


class BoardSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Board
        fields = ["id", "title", "workspace", "description", "owner"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "order"]

    def validate(self, data):
        start_date = data.get("start_date")
        finished_date = data.get("finished_date")
        deadline = data.get("deadline")

        if start_date and finished_date and start_date == finished_date:
            raise serializers.ValidationError(
                "The start time and the end time should not be equal"
            )
        if start_date and deadline and start_date == deadline:
            raise serializers.ValidationError(
                "The start time and the deadline should not be equal"
            )
        return data


class ListSerializer(serializers.ModelSerializer):
    board = BoardSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ["id", "title", "board", "order", "tasks"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
