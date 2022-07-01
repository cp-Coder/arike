from arike.users.models import TYPE_VALUE_MAP
from arike.facility.models.mixins.permissions.base import BasePermissionMixin

class FacilityPermissionMixin(BasePermissionMixin):
  @staticmethod
  def has_bulk_upsert_permission(request):
    return request.user.admin

  def has_object_read_permission(self, request):
    return (
      (request.user.admin)
      or (
          hasattr(self, "district")
          and request.user.role == TYPE_VALUE_MAP["DistrictAdmin"]
          and request.user.district == self.district
        )
      or (request.user.facility == self.users.all())
    )

  def has_object_write_permission(self, request):
    if request.user.role < TYPE_VALUE_MAP["DistrictAdmin"]:
      return False
    return self.has_object_read_permission(request)

  def has_object_update_permission(self, request):
    return super().has_object_update_permission(request) or self.has_object_write_permission(request)

  def has_object_destroy_permission(self, request):
    return self.has_object_read_permission(request)
