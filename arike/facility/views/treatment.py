import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from arike.facility.models.patients import Patient, Treatment, CARE_SUB_TYPES
from arike.facility.forms.patients import TreatmentForm
from arike.facility.views.family import AuthView

class CreateTreatment(AuthView):
  template = "treatment/create.html"
  form_class = TreatmentForm

  def get(self, request, pk1):
    try:
      form = self.form_class()
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk1):
    try:
      data = request.POST
      form = self.form_class(data)
      if form.is_valid():
        model_obj = form.save(commit=False)
        model_obj.patient_id = pk1
        model_obj.care_type = int(model_obj.care_sub_type)
        model_obj.save()
        return HttpResponseRedirect(reverse("arike:view-treatment", args=(pk1,)))
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class UpdateTreatment(AuthView):
  model = Treatment
  template = "treatment/update.html"
  form_class = TreatmentForm

  def get(self, request, pk, pk1):
    try:
      model_obj = self.model.objects.get(id=pk, patient_id=pk1)
      form = self.form_class(instance=model_obj)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk, pk1):
    try:
      model_obj = self.model.objects.get(id=pk, patient_id=pk1)
      data = request.POST
      form = self.form_class(data, instance=model_obj)
      if form.is_valid():
        model_obj = form.save(commit=False)
        model_obj.patient_id = pk1
        model_obj.save()
        return HttpResponseRedirect(reverse("arike:view-treatment", args=(pk1,)))
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class ViewTreatment(AuthView):
  model = Treatment
  template = "treatment/view.html"

  def get(self, request, pk1):
    try:
      current_user = request.user
      data = self.model.objects.filter(patient_id=pk1)
      dt = Patient.objects.get(id=pk1, created_by=current_user)
      return render(request, self.template, {"data": data, "dt": dt})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")


class DetailTreatment(View):
  model = Treatment
  template = "treatment/detail.html"
  form_class = TreatmentForm

  def get(self, request, pk, pk1):
    try:
      data = self.model.objects.get(id=pk, patient_id=pk1)
      return render(request, self.template, {"data": data, "pk1": pk1},)
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DeleteTreatment(AuthView):
  model = Treatment
  template = "treatment/delete.html"

  def get(self, request, pk, pk1):
    try:
      data = self.model.objects.get(id=pk, patient_id=pk1).care_sub_type
      data = CARE_SUB_TYPES[data - 1][1]
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk, pk1):
    try:
      res = request.POST.get("confirm_delete")
      if res == "yes":
        model_obj = self.model.objects.get(id=pk, patient_id=pk1)
        model_obj.delete()
      return HttpResponseRedirect(reverse("arike:view-treatment", args=(pk1,)))
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")
