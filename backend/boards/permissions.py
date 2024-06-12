from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMemberBoardOrNot(BasePermission):
    message = "Permission denied, you are not a member of the board"

    def has_object_permission(self, request, view, obj):
        return request.user in obj.workspace.member.all() or request.user == obj.owner


class IsMemberOfTheTask(BasePermission):
    message = "Permission denied, you are not a member of the task"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsOwnerOrReadOnly(BasePermission):
    message = "Permission denied, you are not the owner"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return self.get_owner(obj) == request.user

    def get_owner(self, obj):
        raise NotImplementedError("Subclasses must implement `get_owner`.")


class IsOwnerOrReadOnlyInBoard(IsOwnerOrReadOnly):
    def get_owner(self, obj):
        return obj.owner


class IsOwnerOrReadOnlyInList(IsOwnerOrReadOnly):
    def get_owner(self, obj):
        return obj.board.owner


class IsOwnerOrReadOnlyInTask(IsOwnerOrReadOnly):
    def get_owner(self, obj):
        return obj.user


class IsOwnerOrReadOnlyInLabel(IsOwnerOrReadOnly):
    def get_owner(self, obj):
        return obj.board.owner
