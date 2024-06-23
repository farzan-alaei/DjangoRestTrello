from django.db import models
from uuid import uuid4
from django.db.models import QuerySet, Manager
from django.utils import timezone

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftQuerySet(QuerySet):
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())


class SoftManager(Manager):
    def get_queryset(self):
        return SoftQuerySet(self.model, using=self._db).filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, editable=False, db_index=True)
    deleted_at = models.DateTimeField(
        null=True, blank=True, editable=False, db_index=True
    )

    objects = SoftManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
