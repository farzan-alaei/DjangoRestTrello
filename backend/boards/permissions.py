from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMemberBoardOrNot(BasePermission):
    """
    Check if the user is a member of the board or the owner of the board.
    """

    message = "Permission denied, you are not a member of the board"

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a member of the board or the owner of the board.
        """
        return request.user in obj.workspace.member.all() or request.user == obj.owner


class IsMemberOfTheTask(BasePermission):
    """
    Check if the user is a member of the task.
    """

    message = "Permission denied, you are not a member of the task"

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a member of the task.
        """
        return request.user == obj.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Check if the user is the owner of the object or if the request method is safe.
    """
    message = "Permission denied, you are not the owner"

    def has_permission(self, request, view):
        """
        Check if the user is the owner of the object or if the request method is safe.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object or if the request method is safe.
        """
        if request.method in SAFE_METHODS:
            return True
        return self.get_owner(obj) == request.user

    def get_owner(self, obj):
        """
        Get the owner of the object.
        """
        raise NotImplementedError("Subclasses must implement `get_owner`.")


class IsOwnerOrReadOnlyInBoard(IsOwnerOrReadOnly):
    """
    Check if the user is the owner of the board or if the request method is safe.
    """
    def get_owner(self, obj):
        """
        Get the owner of the board.
        """
        return obj.owner


class IsOwnerOrReadOnlyInList(IsOwnerOrReadOnly):
    """
    Check if the user is the owner of the list or if the request method is safe.
    """
    def get_owner(self, obj):
        """
        Get the owner of the list.
        """
        return obj.board.owner


class IsOwnerOrReadOnlyInTask(IsOwnerOrReadOnly):
    """
    Check if the user is the owner of the task or if the request method is safe.
    """
    def get_owner(self, obj):
        """
        Get the owner of the task.
        """
        return obj.user


class IsOwnerOrReadOnlyInLabel(IsOwnerOrReadOnly):
    """
    Check if the user is the owner of the label or if the request method is safe.
    """
    def get_owner(self, obj):
        """
        Get the owner of the label.
        """
        return obj.board.owner
