from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from nourish.models import Volunteer

class VolunteerInline(admin.StackedInline):
  model = Volunteer
  can_delete = False
  verbose_name_plural = "volunteer"

class UserAdmin(BaseUserAdmin):
  inlines = [VolunteerInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)