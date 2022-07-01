from arike.users.models import TYPE_VALUE_MAP
from arike.facility.models.facility import Facility
from arike.facility.models.mixins.permissions.base import BasePermissionMixin

class PatientPermissionMixin(BasePermissionMixin):
  @staticmethod
  def has_write_permission(request):
    return (
      request.user.admin or request.user.is_verified
      or request.user.role == TYPE_VALUE_MAP["DistrictAdmin"]
    )

  def has_object_read_permission(self, request):
    return request.user.admin or (
      (hasattr(self, "created_by") and request.user == self.created_by)
      or (self.facility and request.user in self.facility.users.all())
      or (
          request.user.role == TYPE_VALUE_MAP["DistrictAdmin"]
          and (
            request.user.district == self.district
            or (self.facility and request.user.district == self.facility.district)
          )
        )
    )

  def has_object_write_permission(self, request):
    return request.user.is_superuser or (
      (hasattr(self, "created_by") and request.user == self.created_by)
      or (self.facility and request.user in self.facility.users.all())
      or (
          request.user.user_type >= TYPE_VALUE_MAP["DistrictLabAdmin"]
          and (
              request.user.district == self.district
              or (self.facility and request.user.district == self.facility.district)
          )
      )
    )

  def has_object_update_permission(self, request):
    return (
      request.user.is_superuser
      or (hasattr(self, "created_by") and request.user == self.created_by)
      or (self.facility and request.user in self.facility.users.all())
      or (
        request.user.user_type == TYPE_VALUE_MAP["DistrictAdmin"]
        and (
          request.user.district == self.district
          or (self.facility and request.user.district == self.facility.district)
        )
      )
    )
