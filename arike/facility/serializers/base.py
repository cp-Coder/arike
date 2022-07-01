from rest_framework import serializers
from arike.users.models import District, LSG_Body, State, Ward

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = State
    fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
  class Meta:
    model = District
    fields = "__all__"


class LSGSerializer(serializers.ModelSerializer):
  class Meta:
    model = LSG_Body
    fields = "__all__"


class WardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ward
    fields = "__all__"
