from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin  import UserAdmin

# from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email","first_name", "last_name" , "profile_img","is_staff", "is_active",  )
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password","first_name", "last_name" , "profile_img")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1","first_name", "last_name" , "profile_img" ,"is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.register(CustomUser)