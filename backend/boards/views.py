from django.db.models import Q
from rest_framework import viewsets

from boards.models import Board, List, Task, Comment, Label
from boards.permissions import (
    IsOwnerOrReadOnlyInBoard,
    IsOwnerOrReadOnlyInList,
    IsOwnerOrReadOnlyInLabel,
    IsOwnerOrReadOnlyInTask,
    IsMemberBoardOrNot,
    IsMemberOfTheTask,
)
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
        return Board.objects.filter(Q(workspace__member=self.request.user) | Q(owner=self.request.user)).distinct()


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsOwnerOrReadOnlyInList]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnlyInTask]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsMemberOfTheTask]


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrReadOnlyInLabel]
