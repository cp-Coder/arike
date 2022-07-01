from django import forms
from django.forms import ModelForm
from arike.facility.models.facility import Facility

class FacilityForm(ModelForm):
  class Meta:
    model = Facility
    fields = ["name", "address", "ward", "phone", "pincode", "kind"]
    widgets = {
      "address": forms.Textarea(attrs={'rows': 5}),
    }
