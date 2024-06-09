from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else self.mobile

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
