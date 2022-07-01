from arike.users.models import User, TYPE_VALUE_MAP

def get_user(user):
  queryset = User.objects.all()
  if user.admin:
    pass
  elif user.role >= TYPE_VALUE_MAP["DistrictAdmin"]:
    queryset = queryset.filter(district=user.district)
  else:
    queryset = queryset.filter(user=user)
  return queryset
