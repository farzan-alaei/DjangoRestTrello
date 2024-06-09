from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
)
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "mobile")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "mobile")


class CustomAdminAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label=_("Email or Mobile"),
        widget=forms.TextInput(attrs={"autofocus": True}),
    )

    def confirm_login_allowed(self, user):
        if not user.is_staff or not user.is_active:
            raise forms.ValidationError(
                _("This account doesn't have access to this page."),
                code="permission_denied",
            )
