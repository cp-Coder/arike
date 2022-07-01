import logging
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from arike.facility.models.facility import Facility
from facility.serializers.facility import FacilitySerializer
from rest_framework.views import APIView

class FacilityFilterView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      serializer = FacilitySerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        # render(request, self.template, { "data": request.data })
      else:
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      logging.error(e)

