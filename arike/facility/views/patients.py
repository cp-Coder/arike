import logging
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from arike.facility.filters import PatientFilter
from arike.facility.models.facility import Facility, FacilityUser
from arike.users.models import Ward
from arike.facility.models.patients import Patient, VisitDetails
from arike.facility.forms.patients import PatientForm

class AuthView(View):
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseRedirect('/user/login')
    if request.user.role == 40:
      return HttpResponseRedirect("/404")
    return super().dispatch(request, *args, **kwargs)

  def ward_choices(self, request):
    return Ward.objects.filter(lsg_body__district__name__icontains=request.user.district, deleted=False, number__gt=0)

  def get_facility_name(self, request):
    return FacilityUser.objects.get(id=request.user.id).facility_id


def get_facility(request):
  return Facility.objects.filter(ward__lsg_body__district__name__icontains=request.user.district, deleted=False)


def load_facilities(request):
  facilities = get_facility(request)
  return render(request, "hr/facilities.html", {"facilities": facilities})

class CreatePatient(AuthView):
  template = "patients/create.html"
  form_class = PatientForm

  def get(self, request):
    try:
      form = self.form_class()
      form.fields["ward"].queryset = super().ward_choices(request)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request):
    try:
      data = request.POST
      form = self.form_class(data)
      if form.is_valid():
        model_obj = form.save(commit=False)
        model_obj.created_by = request.user
        model_obj.save()
        return redirect("arike:view-patient")
      form.fields["ward"].queryset = super().ward_choices(request)
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class UpdatePatient(AuthView):
  model = Patient
  template = "patients/update.html"
  form_class = PatientForm

  def get(self, request, pk):
    try:
      current_user = request.user
      model_obj = self.model.objects.get(id=pk, created_by=current_user)
      form = self.form_class(instance=model_obj)
      form.fields["ward"].queryset = super().ward_choices(request)
      # have to add the facility dependent options
      # form.fields["facility"].queryset = super().get_facility(request)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk):
    try:
      model_obj = self.model.objects.get(id=pk)
      data = request.POST
      form = self.form_class(data, instance=model_obj)
      if form.is_valid():
          form.save()
          return redirect("arike:view-patient")
      form.fields["ward"].queryset = super().ward_choices(request)
      # have to add the facility dependent options
      # form.fields["facility"].queryset = request.session['facility']
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class ViewPatient(AuthView):
  model = Patient
  template = "patients/view.html"

  def get(self, request):
    try:
      current_user = request.user
      qs = self.model.objects.filter(created_by=current_user)
      data = PatientFilter(request.GET, queryset=qs)
      data.filters["ward"].queryset = super().ward_choices(request)
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DeletePatient(AuthView):
  model = Patient
  template = "patients/delete.html"

  def get(self, request, pk):
    try:
      current_user = request.user
      data = self.model.objects.get(id=pk, created_by=current_user).full_name
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk):
    try:
      res = request.POST.get("confirm_delete")
      if res == "yes":
        model_obj = self.model.objects.get(pk=pk)
        model_obj.delete()
      return redirect("arike:view-patient")
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DetailPatient(AuthView):
  model = Patient
  form_class = PatientForm
  template = "patients/detail.html"

  def get(self, request, pk):
    try:
      current_user = request.user
      data = self.model.objects.get(id=pk, created_by=current_user)
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")
