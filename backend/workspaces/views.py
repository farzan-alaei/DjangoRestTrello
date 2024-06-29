from django.shortcuts import get_object_or_404
from workspaces.models import Workspace, WorkspacesMembership
from workspaces.serializers import WorkspaceSerializer, WorkspacesMembershipSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from workspaces.permissions import IsWorkspaceAdminOrMemberReadOnly
from rest_framework import generics, mixins, status
from django.db.models import Q


# Create your views here.


class WorkspaceDetail(APIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]

    def get_object(self, id):
        workspace = get_object_or_404(Workspace, id=id)
        self.check_object_permissions(self.request, workspace)
        return workspace

    def get(self, request, id):
        workspace = self.get_object(id)
        serializer = WorkspaceSerializer(workspace, context={"request": request})
        return Response(serializer.data)

    def put(self, request, id):
        workspace = self.get_object(id)
        serializer = WorkspaceSerializer(workspace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        workspace = self.get_object(id)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkspacesMembershipDetail(APIView):
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]
    serializer_class = WorkspacesMembershipSerializer

    def get_object(self, id):
        membership = get_object_or_404(WorkspacesMembership, id=id)
        self.check_object_permissions(self.request, membership.workspace)
        return membership

    def delete(self, request, id):
        membership = self.get_object(id)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        membership = self.get_object(id)
        serializer = WorkspacesMembershipSerializer(membership, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspacesMemberList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = WorkspacesMembershipSerializer
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]

    def get_queryset(self):
        workspace = get_object_or_404(Workspace, id=self.kwargs["id"])
        return WorkspacesMembership.objects.filter(workspace=workspace)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WorkspacesList(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsWorkspaceAdminOrMemberReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(
            Q(owner=user) | Q(membership__member=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
