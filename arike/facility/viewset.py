from arike.facility.models.facility import Facility
from facility.serializers.facility import FacilitySerializer
from facility.filters import FacilityFilter
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import mixins, status, viewsets


class FacilityViewSet(mixins.CreateModelMixin,
  mixins.ListModelMixin, mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,mixins.RetrieveModelMixin,
  viewsets.GenericViewSet,):
  queryset = Facility.objects.all().select_related("ward")
  model = Facility
  serializer_class = FacilitySerializer
  # permission_classes = [IsAuthenticated]
  filterset_class = FacilityFilter
  filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
  search_fields = ["ward__name", "kind"]
  lookup_field = "external_id"
