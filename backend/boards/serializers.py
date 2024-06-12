from rest_framework import serializers
from .models import Board, List, Task, Comment, Label


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
