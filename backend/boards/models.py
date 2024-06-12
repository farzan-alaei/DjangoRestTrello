from django.db import models
from core.models import BaseModel, TimeStampMixin, SoftDeleteModel
from django.utils.translation import gettext_lazy as _


class Board(BaseModel, TimeStampMixin, SoftDeleteModel):
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        on_delete=models.CASCADE,
        related_name="boards",
        verbose_name=_("Workspace"),
    )
    owner = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="owned_boards",
        verbose_name=_("Board Owner"),
    )
    title = models.CharField(
        _("Title"),
        help_text=_("title of board"),
        max_length=50,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("description of board activities (optional)"),
        blank=True,
        null=True,
    )
    background_image = models.FileField(
        upload_to="uploads/photos",
        blank=True,
        null=True,
    )

    def get_lists(self):
        return self.lists.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")


class List(BaseModel, TimeStampMixin, SoftDeleteModel):
    board = models.ForeignKey(
        "Board", on_delete=models.CASCADE, related_name="lists", verbose_name=_("Board")
    )
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("enter the title"),
        max_length=50,
        null=False,
        blank=False,
    )
    order = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        blank=True,
        null=True,
    )

    def get_tasks(self):
        return self.tasks.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")


class Task(BaseModel, TimeStampMixin, SoftDeleteModel):
    board_list = models.ForeignKey(
        "List",
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("List"),
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("User"),
    )
    title = models.CharField(
        _("Title"),
        help_text=_("title of task"),
        max_length=50,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("describe your task (optional)"),
        blank=True,
        null=True,
    )
    deadline = models.DateTimeField(
        _("Deadline"),
        help_text=_("specify a deadline (optional)"),
        blank=True,
        null=True,
    )
    start_date = models.DateTimeField(
        _("Start Date"),
        help_text=_("date of start doing task (optional)"),
        blank=True,
        null=True,
    )
    finished_date = models.DateTimeField(
        _("Finish Date"),
        help_text=_("date of when the task finished (optional)"),
        blank=True,
        null=True,
    )
    time_spent = models.TimeField(
        _("Time Spent"),
        help_text=_("the time you spent for doing this task (optional)"),
        blank=True,
        null=True,
    )
    order = models.DecimalField(
        max_digits=7,
        decimal_places=6,
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        "Label", related_name="tasks", verbose_name=_("Labels")
    )

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


class Comment(BaseModel, TimeStampMixin, SoftDeleteModel):
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Task"),
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User"),
    )
    text = models.TextField(
        verbose_name=_("Comment"),
        help_text=_("enter the comment"),
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class Label(BaseModel, TimeStampMixin, SoftDeleteModel):
    board = models.ForeignKey(
        "Board",
        on_delete=models.CASCADE,
        related_name="labels",
        verbose_name=_("Board"),
    )
    title = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Title")
    )
    color = models.CharField(max_length=50, verbose_name=_("Color"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")
