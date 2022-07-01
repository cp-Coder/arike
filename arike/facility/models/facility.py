from django.contrib.auth import get_user_model
from django.db import models
from arike.facility.models.mixins.permissions.facility import FacilityPermissionMixin
from arike.utils.models import BaseModel
from arike.utils.models import phone_number_regex
from arike.users.models import Ward
User = get_user_model()

FACILITY_TYPE = (
  (1, "PHC"),
  (2, "CHC"),
)

class Facility(BaseModel, FacilityPermissionMixin):
  ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
  name = models.CharField(max_length=255)
  address = models.TextField()
  pincode = models.PositiveIntegerField()
  phone = models.CharField(max_length=14, validators=[phone_number_regex])
  kind = models.IntegerField(choices=FACILITY_TYPE, default=1)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  users = models.ManyToManyField(
    User, through="FacilityUser", related_name="facilities", through_fields=("facility", "user"),
  )

  def __str__(self):
    return f"{self.name}"

  def save(self, *args, **kwargs) -> None:
    is_create = self.pk is None
    super().save(*args, **kwargs)

    if is_create:
      FacilityUser.objects.create(facility=self, user=self.created_by, created_by=self.created_by)

class FacilityUser(models.Model):
  facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_users")
