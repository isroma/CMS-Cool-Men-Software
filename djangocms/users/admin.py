from django.contrib import admin
from users.models import Profile, Role


class ProfileInline(admin.StackedInline):
    model = Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "verified")
    list_filter = ("verified", "roles")


class RoleInline(admin.StackedInline):
    model = Role


# This has to be done so Django admin doesn't show roles as "Role object (1)"
class RoleAdmin(admin.ModelAdmin):
    list_display = ("role", )


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
        RoleInline
    ]


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
