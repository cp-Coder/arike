from uuid import uuid4
from arike.facility.models.patients import *
from celery.schedules import crontab
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import localtime, now
from django.core.mail import send_mail
from celery import current_app, shared_task
from celery.utils.log import get_logger
from django.db.models import Count
from datetime import datetime, timedelta, timezone


class Reports:
  def send_email_report(self, object_name, file_name, user):
    if not user.email:
      return
    file = default_storage.open(file_name, "rb")
    msg = EmailMessage(
      f"Care Summary : {self.mode.value} {object_name} : {self.start_date.date()}",
      "Please find the attached report",
      settings.DEFAULT_FROM_EMAIL,
      (user.email,),
    )
    msg.content_subtype = "html"
    msg.attach(f"{self.mode.value}Report.pdf", file.read(), "application/pdf")
    msg.send()
  pass

logger = get_logger(__name__)
def send_report(user):
  status = (
    Patient.objects.filter(user=user, deleted=False)
    .order_by("priority")
    .values("status")
    .annotate(count=Count("status"))
  )
  report = f"Hello, {user.username}. Daily Report:\n\n"
  if not status:
    report += "\nNo task to report today."
  else:
    for s in status:
      _sn = s["status"].title().replace("-", " ")
      _sc = s["count"]
      report += f"\n{_sn} task{'s'[:_sc^1]}: {_sc}"
  result = send_mail("Daily Task Report", report, "example@example.com", ["dummy@user.com"])
  return result, report

@shared_task
def fetch_report():
  logger.info("fetch_settings: Started...")
  start = datetime.now(timezone.utc) - timedelta(minutes=30)
  report_set = Report.objects.filter(
    send_report=True,
    last_updated__lt=start,
  )
  logger.info(f"fetch_report: {len(report_set)} users to report")
  for report in report_set:
    send_report(report.user)
    report.last_updated = datetime.now(timezone.utc).replace(hour=report.report_time.hour, minute=report.report_time.minute,
            second=report.report_time.second)
    report.save()

@current_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.conf.beat_schedule["fetch_report"] = {
    "task": "tasks.tasks.fetch_report",
    "schedule": crontab(minute="*"),
  }
