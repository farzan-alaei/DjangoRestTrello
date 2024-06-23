from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from accounts.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomAdminAuthenticationForm,
)
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "mobile",
        "full_name",
        "date_joined",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "mobile",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "mobile", "first_name", "last_name", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "mobile",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def delete_model(self, request, obj):
        obj.delete()

    def get_queryset(self, request):
        return CustomUser.objects.filter(is_deleted=False)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.login_form = CustomAdminAuthenticationForm
