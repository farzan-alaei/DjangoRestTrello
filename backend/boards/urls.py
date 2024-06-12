from django.urls import path
from boards.views import (
    BoardViewSet,
    ListViewSet,
    TaskViewSet,
    CommentViewSet,
    LabelViewSet,
)
from rest_framework import routers


app_name = "boards"


router = routers.SimpleRouter()
router.register("board", BoardViewSet, basename="boards")
router.register("list", ListViewSet, basename="boards_list")
router.register("task", TaskViewSet, basename="boards_task")
router.register("comment", CommentViewSet, basename="boards_comment")
router.register("label", LabelViewSet, basename="boards_label")

urlpatterns = router.urls
