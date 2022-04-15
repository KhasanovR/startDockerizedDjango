from django.contrib import admin
from reversion.admin import VersionAdmin

from my_app.account.models import User


@admin.register(User)
class UserAdmin(VersionAdmin):
    pass
