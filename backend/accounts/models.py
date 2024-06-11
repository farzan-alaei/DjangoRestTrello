from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager
from core.models import SoftDeleteModel, BaseModel


class CustomUser(AbstractUser, BaseModel, SoftDeleteModel):
    """
    Custom user model with email and mobile fields for authenticated with email or mobile
    """

    username = None
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else self.mobile

    def full_name(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
