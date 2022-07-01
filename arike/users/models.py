from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from arike.utils.models import phone_number_regex
from django.urls import reverse
from arike.utils.models import BaseModel
# from arike.users import constants



LOCAL_BODY_CHOICES = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
)

class State(BaseModel):
  name = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.name}"


class District(BaseModel):
  state = models.ForeignKey(State, on_delete=models.PROTECT)
  name = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.name}"


class LSG_Body(BaseModel):
  district = models.ForeignKey(District, on_delete=models.PROTECT)
  name = models.CharField(max_length=255)
  kind = models.IntegerField(choices=LOCAL_BODY_CHOICES, default=1)
  lsg_body_code = models.CharField(max_length=20, blank=True, null=True)

  def __str__(self):
    return f"{self.name}"


class Ward(BaseModel):
  lsg_body = models.ForeignKey(LSG_Body, on_delete=models.PROTECT)
  name = models.CharField(max_length=255)
  number = models.PositiveIntegerField()

  def __str__(self):
    return f"{self.name}"

class CustomUserManager(BaseUserManager):
  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('The given email must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('staff', True)
    extra_fields.setdefault('admin', True)
    extra_fields.setdefault('full_name', email)
    extra_fields["phone"] = "+919696969696"
    extra_fields["role"] = 40
    return self._create_user(email, password, **extra_fields)

TYPE_VALUE_MAP = {
  "SecondaryNurse": 5,
  "PrimaryNurse": 10,
  "DistrictAdmin": 40,
}

class UsernameValidator(UnicodeUsernameValidator):
  regex = r"^[\w.@+-]+[^.@+_-]$"
  message = _("Please enter letters, digits and @ . + - _ only and username should not end with @ . + - or _")
class User(AbstractBaseUser):
  external_id = models.UUIDField(default=uuid4, unique=True, db_index=True)
  full_name = models.CharField(max_length=150)
  # username_validator = UsernameValidator()
  # username = models.CharField(
  #   _("username"),
  #   max_length=150,
  #   unique=True,
  #   help_text=_("150 characters or fewer. Letters, digits and @/./+/-/_ only."),
  #   validators=[username_validator],
  # )
  email = models.EmailField(_("email"), max_length=60, unique=True)
  TYPE_CHOICES = [(value, name) for name, value in TYPE_VALUE_MAP.items()]
  role = models.IntegerField(choices=TYPE_CHOICES, blank=False)
  district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
  phone = models.CharField(max_length=14, validators=[phone_number_regex])
  is_verified = models.BooleanField(default=True)
  deleted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_active = models.BooleanField(default=True)
  staff = models.BooleanField(default=False)
  admin = models.BooleanField(default=False)

  USERNAME_FIELD = "email"

  REQUIRED_FIELDS = [
  ]
  objects = CustomUserManager()

  def __str__(self):
    return self.email

  @property
  def is_staff(self):
    return self.staff

  @property
  def is_admin(self):
    return self.admin

  def has_module_perms(self, app_label):
    return True

  def has_perm(self, perm, obj=None):
    return True

  @staticmethod
  def has_read_permission(request):
    return True

  def has_object_read_permission(self, request):
    return request.user.admin or self == request.user

  @staticmethod
  def has_write_permission(request):
    return True

  def has_object_write_permission(self, request):
    return request.user.admin

  def has_object_update_permission(self, request):
    if request.user.admin:
      return True
    if not self == request.user:
      return False
    if request.data.get("district") and self.role == TYPE_VALUE_MAP["DistrictAdmin"]:
      return False
    return True

  @staticmethod
  def has_add_user_permission(request):
    return request.user.admin or request.user.is_verified

  def get_absolute_url(self):
    return reverse("users:detail", kwargs={"username": self.username})

  def delete(self, *args, **kwargs):
    self.deleted = True
    self.save()
