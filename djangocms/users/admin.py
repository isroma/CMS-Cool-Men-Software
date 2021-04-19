from django.contrib import admin
from users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "verified")
    list_filter = ("verified", )


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
    ]

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
