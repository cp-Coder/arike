from uuid import uuid4
from django.db import models
from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(
    regex=r"^((\+91|91|0)[\- ]{0,1})?[456789]\d{9}$",
    message="Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)

class BaseManager(models.Manager):
  def get_queryset(self):
    qs = super().get_queryset()
    return qs.filter(deleted=False)

  def filter(self, *args, **kwargs):
    _id = kwargs.pop("id", "----")
    if _id != "----" and not isinstance(_id, int):
      kwargs["external_id"] = _id
    return super().filter(*args, **kwargs)

class BaseModel(models.Model):
  external_id = models.UUIDField(default=uuid4, unique=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted = models.BooleanField(default=False)
  objects = BaseManager()
  class Meta:
    abstract = True

  def delete(self, **args):
    self.deleted = True
    self.save()
