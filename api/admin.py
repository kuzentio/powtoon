from django.contrib import admin
from django.contrib.auth.models import Permission

from api.models import Powtoon


@admin.register(Powtoon)
class PowtoonAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
