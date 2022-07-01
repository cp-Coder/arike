import time
from arike.facility.models.patients import *
from celery.schedules import crontab
from django.conf import settings
from hardcopy import bytestring_to_pdf
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import localtime, now
from django.core.mail import send_mail
from celery import current_app, shared_task
from celery.utils.log import get_logger
from django.db.models import Count
from datetime import datetime, timedelta, timezone

class Report:
  start_date = None
  end_date = None
  filter_field = ""
  object_ids = []

  def __init__(self):
    self.start_date = (localtime(now()) - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    self.end_date = self.start_date + timedelta(days=1)

  def get_object_name(self, object_id):
    return Patient.objects.get(id=object_id).full_name

  def fetch_patient_ids(self):
    self.object_ids = list(Patient.objects.filter(deleted=False).values_list("id"))

  def patient_visit_detail_summary(self, base_filters):
    return_dict = {}
    visit_id = VisitSchedule.objects.filter(**base_filters).order_by("-created_at")
    return_dict["health-info"] = VisitDetails.objects.filter(deleted=False, visit_schedule_id=visit_id, updated_at__gte=self.start_date, update_at__lte=self.end_date).values().first()
    return return_dict

  def patient_treatment_summary(self, base_filters):
    return_dict = {}
    base_queryset = Treatment.objects.filter(**base_filters).order_by("-updated_at")
    qs = base_queryset.filter(deleted=False, updated_at__gte=self.start_date, updated_at__lte=self.end_date).values()
    return_dict["treatment-summary"] = [q for q in qs]
    return return_dict

  def generate_report_data(self, object_id):
    final_data = {}
    base_filters = {"patient_id": object_id, "deleted": False}
    final_data["patients_treatment_summary"] = self.patient_treatment_summary(base_filters)
    final_data["patients_visit_detail"] = self.patient_visit_detail_summary(base_filters)
    return final_data

  def generate_reports(self):
    for object_id in self.object_ids:
      data = self.generate_report_data(object_id)
      object_name = self.get_object_name(object_id)
      data["object_name"] = object_name
      data["current_date"] = str(self.start_date.date())
      html_string = render_to_string("reports/report.html", data)
      file_name = str(int(round(time.time() * 1000))) + str(object_id) + ".pdf"
      bytestring_to_pdf(
          html_string.encode(),
          default_storage.open(file_name, "w+"),
          **{
              "no-margins": None,
              "disable-gpu": None,
              "disable-dev-shm-usage": False,
              "window-size": "2480,3508",
          },
      )



# logger = get_logger(__name__)
# def send_report(user):
#   status = (
#     Patient.objects.filter(user=user, deleted=False)
#     .order_by("priority")
#     .values("status")
#     .annotate(count=Count("status"))
#   )
#   report = f"Hello, {user.username}. Daily Report:\n\n"
#   if not status:
#     report += "\nNo task to report today."
#   else:
#     for s in status:
#       _sn = s["status"].title().replace("-", " ")
#       _sc = s["count"]
#       report += f"\n{_sn} task{'s'[:_sc^1]}: {_sc}"
#   result = send_mail("Daily Task Report", report, "example@example.com", ["dummy@user.com"])
#   return result, report

# @shared_task
# def fetch_report():
#   logger.info("fetch_settings: Started...")
#   start = datetime.now(timezone.utc) - timedelta(minutes=30)
#   report_set = Report.objects.filter(
#     send_report=True,
#     last_updated__lt=start,
#   )
#   logger.info(f"fetch_report: {len(report_set)} users to report")
#   for report in report_set:
#     send_report(report.user)
#     report.last_updated = datetime.now(timezone.utc).replace(hour=report.report_time.hour, minute=report.report_time.minute,
#             second=report.report_time.second)
#     report.save()

# @current_app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#   sender.conf.beat_schedule["fetch_report"] = {
#     "task": "tasks.tasks.fetch_report",
#     "schedule": crontab(minute="*"),
#   }
