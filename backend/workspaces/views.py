from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from workspaces.models import Workspace, WorkspacesMembership
from workspaces.permissions import IsWorkspaceAdminOrMemberReadOnly
from workspaces.serializers import WorkspaceSerializer, WorkspacesMembershipSerializer


# Create your views here.


class WorkspaceDetail(APIView):
    """
    Returns a workspace by its id.
    """
    serializer_class = WorkspaceSerializer
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]

    def get_object(self, id):
        """
        Get a workspace by its id.
        """
        workspace = get_object_or_404(Workspace, id=id)
        self.check_object_permissions(self.request, workspace)
        return workspace

    def get(self, request, id):
        """
        Get a workspace by its id.
        """
        workspace = self.get_object(id)
        serializer = WorkspaceSerializer(workspace, context={"request": request})
        return Response(serializer.data)

    def put(self, request, id):
        """
        Update a workspace by its id.
        """
        workspace = self.get_object(id)
        serializer = WorkspaceSerializer(workspace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Delete a workspace by its id.
        """
        workspace = self.get_object(id)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkspacesMembershipDetail(APIView):
    """
    Retrieve, update or delete a workspace membership.
    """
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]
    serializer_class = WorkspacesMembershipSerializer

    def get_object(self, id):
        """
        Get a workspace membership by its id.
        """
        workspace = get_object_or_404(Workspace, id=self.kwargs["id"])
        membership = get_object_or_404(WorkspacesMembership, id=id)
        self.check_object_permissions(self.request, membership.workspace)
        return membership

    def delete(self, request, id):
        """
        Delete a workspace membership.
        """
        membership = self.get_object(id)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        """
        Update a workspace membership.
        """
        membership = self.get_object(id)
        serializer = WorkspacesMembershipSerializer(membership, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspacesMemberList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    List or create workspace memberships.
    """
    serializer_class = WorkspacesMembershipSerializer
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]

    def get_queryset(self):
        """
        Returns queryset of workspace memberships for the given workspace id.
        """
        workspace = get_object_or_404(Workspace, id=self.kwargs["id"])
        return WorkspacesMembership.objects.filter(workspace=workspace)

    def get(self, request, *args, **kwargs):
        """
        List workspace memberships.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new workspace membership.
        """
        workspace = get_object_or_404(Workspace, id=self.kwargs["id"])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(workspace=workspace)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspacesList(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """
    List or create workspaces.
    """
    serializer_class = WorkspaceSerializer
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]

    def get_queryset(self):
        """
        Returns queryset of workspaces for the given user.
        """
        if self.request.user.is_anonymous:
            return Workspace.objects.none()
        user = self.request.user
        return Workspace.objects.filter(
            Q(owner=user) | Q(membership__member=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Create a new workspace with the current user as the owner.
        """
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        List workspaces.
        Returns a list of workspaces for the authenticated user.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new workspace.
        """
        return self.create(request, *args, **kwargs)
