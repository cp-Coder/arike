# from django.contrib.auth import get_user_model
from rest_framework import serializers
from arike.facility.models.facility import Facility, FACILITY_TYPE
from arike.facility.serializers.base import WardSerializer, LSGSerializer, DistrictSerializer, StateSerializer
from facility.serializer import ChoiceField
#User = get_user_model()

class FacilitySerializer(serializers.ModelSerializer):
  id = serializers.UUIDField(source="external_id", read_only=True)
  ward = serializers.StringRelatedField()
  kind = ChoiceField(choices=FACILITY_TYPE)

  class Meta:
    model = Facility
    fields = ("id", "ward", "name", "address", "pincode", "phone", "kind")

