from django.contrib import admin
from workspaces.models import Workspace, WorkspacesMembership

# Register your models here.


admin.site.register(Workspace)
admin.site.register(WorkspacesMembership)
