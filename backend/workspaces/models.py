from django.db import models
from core.models import TimeStampMixin, SoftDeleteModel, BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Workspace(BaseModel, TimeStampMixin, SoftDeleteModel):
    owner = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE, related_name="workspaces"
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(null=False, blank=True)
    member = models.ManyToManyField(
        "accounts.CustomUser",
        related_name="membered_workspace",
        through="WorkspacesMembership",
        through_fields=("workspace", "member"),
    )

    def get_boards(self):
        return self.boards.all()

    def __str__(self):
        return self.title


class WorkspacesMembership(BaseModel, TimeStampMixin, SoftDeleteModel):
    class AccessLevel(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MEMBER = "member", _("Member")

    workspace = models.ForeignKey(
        "workspaces.Workspace", on_delete=models.CASCADE, related_name="membership"
    )
    member = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="workspace_membership",
    )
    access_level = models.CharField(
        max_length=10, choices=AccessLevel.choices, default=AccessLevel.MEMBER
    )

    def __str__(self):
        return f"{self.workspace.title} - {self.member.email}"

    class Meta:
        unique_together = ("workspace", "member")
