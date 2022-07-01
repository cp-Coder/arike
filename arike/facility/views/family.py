import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from arike.facility.models.patients import FamilyDetail, Patient
from arike.facility.forms.patients import FamilyForm

class AuthView(View):
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseRedirect('/user/login')
    if request.user.role > 15:
      return HttpResponseRedirect("/404")
    return super().dispatch(request, *args, **kwargs)

  def get_patient(self, pk):
    return Patient.objects.get(id=pk).full_name

class CreateFamily(AuthView):
  template = "family/create.html"
  form_class = FamilyForm

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
        model_obj.save()
        return HttpResponseRedirect(reverse("arike:view-family", args=(pk1,)))
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class UpdateFamily(AuthView):
  model = FamilyDetail
  template = "family/update.html"
  form_class = FamilyForm

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
        return HttpResponseRedirect(reverse("arike:view-family", args=(pk1,)))
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class ViewFamily(AuthView):
  model = FamilyDetail
  template = "family/view.html"

  def get(self, request, pk1):
    try:
      current_user = request.user
      data = self.model.objects.filter(patient_id=pk1)
      dt = Patient.objects.get(id=pk1, created_by=current_user)
      return render(request, self.template, {"data": data, "dt": dt})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DetailFamily(AuthView):
  model = FamilyDetail
  template = "family/detail.html"

  def get(self, request, pk, pk1):
    try:
      data = self.model.objects.get(id=pk, patient_id=pk1)
      return render(request, self.template, {"data": data, "pk1": pk1})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DeleteFamily(AuthView):
  model = FamilyDetail
  template = "family/delete.html"

  def get(self, request, pk, pk1):
    try:
      data = self.model.objects.get(id=pk, patient_id=pk1).full_name
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
      return HttpResponseRedirect(reverse("arike:view-family", args=(pk1,)))
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")
