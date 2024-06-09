from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile, password, **extra_fields):
        if not email and not mobile:
            raise ValueError(_("The Email or Mobile must be set"))

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, mobile, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, mobile, password, **extra_fields)