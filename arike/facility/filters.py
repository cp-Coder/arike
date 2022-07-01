from django_filters import rest_framework as filters
from arike.facility.models.facility import Facility
from arike.facility.models.patients import Patient


class FacilityFilter(filters.FilterSet):
  class Meta:
    model = Facility
    fields = {
      "name": ["icontains"],
      "ward": ["exact"],
      "kind": ["exact"],
    }


class PatientFilter(filters.FilterSet):
  class Meta:
    model = Patient
    fields = {
      "full_name": ["icontains"],
      "ward": ["exact"],
      "gender": ["exact"],
    }

