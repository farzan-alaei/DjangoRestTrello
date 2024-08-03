from django.db.models import Q
from rest_framework import viewsets, serializers

from boards.models import Board, List, Task, Comment, Label
from boards.permissions import (
    IsOwnerOrReadOnlyInBoard,
    IsOwnerOrReadOnlyInList,
    IsOwnerOrReadOnlyInLabel,
    IsOwnerOrReadOnlyInTask,
    IsMemberBoardOrNot,
    IsMemberOfTheTask,
)
from workspaces.models import Workspace
from .serializers import (
    BoardSerializer,
    ListSerializer,
    TaskSerializer,
    CommentSerializer,
    LabelSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsOwnerOrReadOnlyInBoard, IsMemberBoardOrNot]

    def get_queryset(self):
        return Board.objects.filter(
            Q(workspace__member=self.request.user) | Q(owner=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        workspace_data = self.request.data.get("workspace")
        workspace = Workspace.objects.get(id=workspace_data["id"])
        serializer.save(owner=self.request.user, workspace=workspace)


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsOwnerOrReadOnlyInList]

    def get_queryset(self):
        board_id = self.request.query_params.get("board_id")
        if board_id:
            return List.objects.filter(
                Q(board__workspace__member=self.request.user)
                | Q(board__owner=self.request.user),
                board_id=board_id,
            ).distinct()
        else:
            return List.objects.none()

    def perform_create(self, serializer):
        board_id = self.request.data.get("board")
        board = Board.objects.get(id=board_id)
        serializer.save(board=board)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnlyInTask]

    def perform_create(self, serializer):
        list_id = self.request.query_params.get("list_id")
        if list_id:
            list_instance = List.objects.get(id=list_id)
            serializer.save(board_list=list_instance, user=self.request.user)
        else:
            raise serializers.ValidationError("list_id parameter is required.")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsMemberOfTheTask]


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrReadOnlyInLabel]
