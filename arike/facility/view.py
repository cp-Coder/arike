import logging
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from arike.facility.models.facility import Facility
from arike.users.models import Ward
from arike.facility.forms.facility import FacilityForm
from arike.facility.filters import FacilityFilter

class AuthView(View):
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseRedirect('/user/login')
    if request.user.role != 40:
      return HttpResponseRedirect("/403")
    return super().dispatch(request, *args, **kwargs)

  # will give all the wards available in that particular district
  def choices(self, request):
    return Ward.objects.filter(lsg_body__district__name__icontains=request.user.district, deleted=False)

class CreateFacility(AuthView):
  model = Facility
  template = "facility/create.html"
  form_class = FacilityForm

  def get(self, request):
    try:
      form = self.form_class()
      form.fields["ward"].queryset = super().choices(request)
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
        return redirect("arike:view-facility")
      form.fields["ward"].queryset = super().choices(request)
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class UpdateFacility(AuthView):
  model = Facility
  template = "facility/update.html"
  form_class = FacilityForm

  def get(self, request, pk):
    try:
      current_user = request.user
      model_obj = self.model.objects.get(id=pk, created_by=current_user)
      form = self.form_class(instance=model_obj)
      form.fields["ward"].queryset = super().choices(request)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk):
    try:
      model_obj = self.model.objects.get(id=pk)
      form = self.form_class(request.POST, instance=model_obj)
      if form.is_valid():
        form.save()
        return redirect("arike:view-facility")
      form.fields["ward"].queryset = super().choices(request)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class ViewFacility(AuthView):
  model = Facility
  template = "facility/view.html"

  def get(self, request):
    try:
      current_user = request.user
      qs = self.model.objects.filter(created_by=current_user)
      data = FacilityFilter(request.GET, queryset=qs)
      data.filters["ward"].queryset = super().choices(request)
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DetailFacility(View):
  model = Facility
  template = "facility/detail.html"
  form_class = FacilityForm

  def get(self, request, pk):
    try:
      current_user = request.user
      data = self.model.objects.get(id=pk, created_by=current_user)
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DeleteFacility(AuthView):
  model = Facility
  template = "facility/delete.html"

  def get(self, request, pk):
    try:
      current_user = request.user
      data = Facility.objects.get(id=pk, created_by=current_user).name
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
      return redirect("arike:view-facility")
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")
