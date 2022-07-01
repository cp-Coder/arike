import logging
from django.http import HttpResponseRedirect
from django.db.models.functions import TruncDay
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from arike.facility.models.facility import FacilityUser
from arike.facility.models.patients import Treatment, TreatmentNotes, VisitSchedule, Patient, VisitDetails
from arike.facility.forms.patients import TreatmentNotesForm, VisitDetailForm, VisitScheduleForm
from arike.facility.views.family import AuthView

class CreateVisit(AuthView):
  template = "visit/create.html"
  form_class = VisitScheduleForm

  def get(self, request):
    try:
      form = self.form_class()
      form.fields["patient"].queryset = Patient.objects.filter(created_by=request.user)
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
        # model_obj.patient_id
        model_obj.save()
        return HttpResponseRedirect(reverse("arike:agenda"))
      form.fields["patient"].queryset = Patient.objects.filter(created_by=request.user)
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class ViewVisit(AuthView):
  model = VisitSchedule
  template = "visit/view.html"

  def get(self, request):
    try:
      data = Patient.objects.filter(created_by=request.user)
      # treatments = {}
      # for dt in data:
      #   try:
      #     treatments[dt.id] = [ qs for qs in Treatment.objects.filter(patient_id=dt.id).values('care_type') ]
      #   except:
      #     pass
      # breakpoint()
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class Agenda(AuthView):
  model = VisitSchedule
  template = "visit/agenda.html"

  def get(self, request):
    try:
      data = VisitSchedule.objects.select_related('patient').filter(patient__created_by=request.user).order_by(TruncDay('time'))
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DeleteVisit(AuthView):
  model = VisitSchedule
  template = "visit/delete.html"

  def get(self, request, pk):
    try:
      data = self.model.objects.get(id=pk).time
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk):
    try:
      res = request.POST.get("confirm_delete")
      if res == "yes":
        model_obj = self.model.objects.get(id=pk)
        model_obj.delete()
      return redirect("arike:agenda")
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DetailVisit(AuthView):
  model = VisitSchedule
  form_class = VisitScheduleForm
  template = "visit/detail.html"

  def get(self, request, pk):
    try:
      data = self.model.objects.get(id=pk)
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class ViewHistoy(AuthView):
  template = "visit_schedule/view.html"
  model = VisitSchedule

  def get(self, request, pk1):
    try:
      current_user = request.user
      data = self.model.objects.filter(patient_id=pk1)
      dt = Patient.objects.get(id=pk1, created_by=current_user)
      return render(request, self.template, {"data": data, "dt": dt})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DetailHistory(AuthView):
  template = "visit_schedule/detail.html"
  form_class = VisitDetailForm

  def get(self, request, pk, pk1):
    try:
      model_obj = VisitDetails.objects.get(id=pk)
      form = self.form_class(instance=model_obj)
      return render(request, self.template, {"data": model_obj, "form":form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class VisitPatient(AuthView):
  template = "visit/patient_visit.html"
  def get(self, request, pk1):
    return render(request, self.template, {"pk1": pk1})


class PatientInfo(AuthView):
  model = VisitDetails
  form_class = VisitDetailForm
  template = "visit/patientinfo.html"

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
        model_obj.visit_schedule_id = VisitSchedule.objects.get(id=pk1).id
        model_obj.save()
        return HttpResponseRedirect(reverse("arike:patient_visit", args=(pk1,)))
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class AddTreatmentNotes(AuthView):
  model = TreatmentNotes
  form_class = TreatmentNotesForm
  template = "visit/treatment_notes.html"

  # pk1 -> visit id on the agenda
  # pk -> Patient id

  def get(self, request, pk1):
    try:
      form = self.form_class()
      current_user = request.user
      pk = VisitSchedule.objects.get(id=pk1).patient_id
      info = Patient.objects.get(id=pk, created_by=current_user).full_name
      dt = Treatment.objects.filter(patient_id=pk).order_by("-updated_at")
      return render(request, self.template, {"form": form, "dt": dt.first(), "info": info})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk1):
    try:
      data = request.POST
      current_user = request.user
      # breakpoint()
      form = self.form_class(data)
      pk = VisitSchedule.objects.get(id=pk1).patient_id
      dt = Treatment.objects.filter(patient_id=pk).order_by("-updated_at").first()
      if form.is_valid():
        model_obj = form.save(commit=False)
        model_obj.visit_id = pk1
        model_obj.treatment_id = dt.id
        # print(pk1, dt.id, pk)
        model_obj.save()
        # breakpoint()
        return HttpResponseRedirect(reverse("arike:treatment-notes", args=(pk1,)))
      info = Patient.objects.get(id=pk, created_by=current_user).full_name
      return render(request, self.template, {"form": form, "dt": dt, "info": info})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class ViewTreatmentNotes(AuthView):
  model = TreatmentNotes
  template = "visit_schedule/visit_treatment.html"
  def get(self, request, pk1):
    try:
      current_user = request.user
      pk = VisitSchedule.objects.get(id=pk1).patient_id
      dt = Treatment.objects.filter(patient_id=pk).order_by("-updated_at").first()
      info = Patient.objects.get(id=pk, created_by=current_user).full_name
      data = self.model.objects.filter(visit_id=pk1)
      # logging.info(data, dt, pk1, info)
      return render(request, self.template, {"data": data, "pk1": pk1, "dt": dt, "info": info})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")
