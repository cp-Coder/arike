from arike.users.models import TYPE_VALUE_MAP

class BasePermissionMixin:
  @staticmethod
  def has_read_permission(request):
    return request.user.admin or request.user.is_verified

  @staticmethod
  def has_write_permission(request):
    return (
      request.user.is_admin or request.user.is_verified
      or request.user.role == TYPE_VALUE_MAP["DistrictAdmin"]
    )

  def has_object_read_permission(self, request):
    return (request.user.admin) or (
      (hasattr(self, "created_by") and request.user == self.created_by)
      or (
        hasattr(self, "district")
        and request.user.role == TYPE_VALUE_MAP["DistrictAdmin"]
        and request.user.district == self.district
      )
    )

  def has_object_update_permission(self, request):
    return (request.user.admin) or (
      (hasattr(self, "created_by") and request.user == self.created_by)
      or (
        hasattr(self, "district")
        and request.user.role == TYPE_VALUE_MAP["DistrictAdmin"]
        and request.user.district == self.district
      )
    )

  def has_object_destroy_permission(self, request):
    return request.user.admin or (hasattr(self, "created_by") and request.user == self.created_by)
