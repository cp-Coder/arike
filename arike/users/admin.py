from django.contrib import admin
from arike.users.models import District, LSG_Body, State, Ward
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from arike.users.forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()
@admin.register(User)
class UserAdmin(BaseUserAdmin):
  form = UserAdminChangeForm
  add_form = UserAdminCreationForm

  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    (_('Personal info'), {'fields': ('full_name', 'role', 'district')}),
    (_('Permissions'), {'fields': ('admin', 'is_verified')}),
    (_('Important dates'), {'fields': ('last_login',)}),
  )
  add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password', 'password_2', 'role', 'district')
        }),
  )
  list_display = ['email', 'full_name', 'admin', 'staff']
  search_fields = ['email', 'full_name']
  ordering = ['email']
  filter_horizontal = ()
  list_filter = ('admin',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
  search_fields = ["name"]
  readonly_fields = ["external_id"]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
  search_fields = ["name"]
  autocomplete_fields = ["state"]


@admin.register(LSG_Body)
class LocalBodyAdmin(admin.ModelAdmin):
  search_fields = ["name"]
  autocomplete_fields = ["district"]


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
  search_fields = ["name"]
  autocomplete_fields = ["lsg_body"]
