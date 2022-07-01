import enum, itertools
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from arike.utils.models import BaseModel, phone_number_regex
from arike.facility.models.facility import Facility
from arike.users.models import Ward
from arike.facility.models.mixins.permissions.patient import PatientPermissionMixin

User = get_user_model()

GENDER_CHOICES = [(1, "Male"), (2, "Female"), (3, "Non-binary")]
class Patient(BaseModel, PatientPermissionMixin):
  full_name = models.CharField(max_length=255)
  date_of_birth = models.DateField(null=True)
  address = models.TextField(null=True, blank=False)
  landmark = models.TextField(null=True, blank=False)
  phone_number = models.CharField(max_length=14, validators=[phone_number_regex])
  gender = models.IntegerField(choices=GENDER_CHOICES, blank=False)
  emergency_phone_number = models.CharField(max_length=14, validators=[phone_number_regex])
  expired_time = models.TimeField(null=True, blank=True)
  ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
  facility = models.ForeignKey(Facility, on_delete=models.PROTECT, null=True, blank=True)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="patient_created_by")

  def __str__(self):
    return f"{self.full_name}"

  def get_absolute_url(self):
    return reverse('arike:patient', kwargs={'pk': self.pk})

class RelationEnum(enum.IntEnum):
  FAMILY_MEMBER = 1
  FRIEND = 2
  RELATIVE = 3
  NEIGHBOR = 4
  TRAVEL_TOGETHER = 5
  WHILE_AT_HOSPITAL = 6
  WHILE_AT_SHOP = 7
  WHILE_AT_OFFICE_OR_ESTABLISHMENT = 8
  WORSHIP_PLACE = 9
  OTHERS = 10
RELATION_CHOICES = [(item.value, item.name) for item in RelationEnum]

class FamilyDetail(BaseModel):
  full_name = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=14, validators=[phone_number_regex])
  date_of_birth = models.DateField(null=True)
  email = models.EmailField(null=True, blank=False)
  relation = models.IntegerField(choices=RELATION_CHOICES, default=1)
  address = models.TextField(null=True, blank=False)
  education = models.TextField(null=True, blank=False)
  occupation = models.TextField(null=True, blank=False)
  remarks = models.TextField(null=True, blank=False)
  is_primary = models.BooleanField(null=True)
  expired_time = models.TimeField(null=True, blank=True)
  patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True, blank=True)

  def __str__(self):
    return f"{self.full_name}"


def reverse_choices(choices):
  output = []
  for choice in choices:
    output.append((choice[1], choice[0]))
  return output

ICDS_CHOICES = [
  ("DM", "D-32"), ("Hypertension", "HT-58"),
  ("IHD","IDH-21"), ("COPD", "DPOC-144"),
  ("Dementia", "DM-62"), ("CVA", "CAV-89"),
  ("Cancer", "C-98"), ("CKD", "DC-25")]

# class Disease(BaseModel):
#   DISEASE_CHOICES = reverse_choices(choices=ICDS_CHOICES)
#   icds_code = models.CharField(max_length=100, choices=ICDS_CHOICES)
#   disease = models.CharField(max_length=100, choices=DISEASE_CHOICES)

#   def __str__(self):
#     return f"{self.disease}"

class PatientDisease(BaseModel):
  # disease = models.ForeignKey(Disease, on_delete=models.PROTECT, null=True, blank=True)
  patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True, blank=True)
  disease = models.CharField(max_length=100, choices=ICDS_CHOICES)
  note = models.TextField(null=True, blank=False)

class VisitSchedule(BaseModel):
  time = models.DateTimeField(null=True, blank=False)
  duration = models.CharField(null=True, blank=False, max_length=5)
  patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True, blank=True)
  # user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

PALLIATIVE_PHASE_CHOICES = [
  ("Stable", "Stable"), ("Unstable", "Unstable"),
  ("Deteriorating", "Deteriorating"), ("Dying", "Dying")
]

SYSTEMIC_EXAMINATION = [
  (1, "Cardiovascular"),
  (2, "Gastrointestinal"),
  (3, "Central Nervous System"),
  (4, "Respiratory"),
  (5, "Genital-urinary")
]

class VisitDetails(BaseModel):
  palliative_phase = models.CharField(max_length=50, choices=PALLIATIVE_PHASE_CHOICES, default=PALLIATIVE_PHASE_CHOICES[0][0])
  blood_pressure = models.CharField(max_length=50, null=True, blank=False)
  pulse = models.CharField(max_length=50, null=True, blank=False)
  general_random_blood_sugar = models.CharField(max_length=50, null=True, blank=False)
  personal_hygiene = models.TextField(null=True, blank=False)
  mouth_hygiene = models.TextField(null=True, blank=False)
  pubic_hygiene = models.TextField(null=True, blank=False)
  systemic_examination = models.IntegerField(choices=SYSTEMIC_EXAMINATION, default=0)
  patient_at_peace = models.BooleanField(null=True, blank=False)
  pain = models.BooleanField(null=True, blank=False)
  symptoms = models.TextField(null=True, blank=False)
  visit_schedule = models.ForeignKey(VisitSchedule, on_delete=models.PROTECT, null=True, blank=True)

CARE_CHOICES = {
  "General care": ["Mouth care", "Bath", "Nail cutting", "Shaving"],
  "Genito urinary care": [
    "Perennial care",
    "Condom catheterisation & training",
    "Nelcath catheterisation & training",
    "Foley's catheterisation",
    "Foley's catheter care",
    "Suprapubic catheterisation",
    "Suprapubic catheter care",
    "Bladder wash with normal saline",
    "Bladder wash with soda bicarbonate",
    "Urostomy care",
  ],
  "Gastro-intestinal care": [
    "Ryles tube insertion",
    "Ryles tube care",
    "Ryles tube feeding & training",
    "PEG care",
    "Per Rectal Enema",
    "High enema",
    "Bisacodyl Suppository",
    "Digital evacuation",
    "Colostomy care",
    "Colostomy irrigation care",
    "ileostomy care",
  ],
  "Wound care": [
    "Wound care training given to family",
    "Wound dressing",
    "Suture removal",
    "Vacuum dressing",
  ],
  "Respiratory care": [
    "Tracheostomy care",
    "Chest physiotherapy",
    "Inhaler training",
    "Oxygen concentrator - training",
    "Bi-PAP training",
    "Bandaging",
    "Upper limb lymphedema bandaging",
    "Lower limb lymphedema bandaging",
    "Upper limb lymphedema hosiery",
    "PVOD bandaging",
  ],
  "Invasive care": [
    "IV fluid infusion",
    "IV medicine bolus administration",
    "IV cannula care",
    "IV cannula insertion",
    "S/C cannula insertion",
    "S/C fluid infusion (subcutaneous)",
    "S/C medicine bolus administration",
    "S/C cannula care",
    "Ascites tapping",
    "Ascitic catheter care",
  ],
  "Physiotherapy": [
    "Passive Movement",
    "Active Movement",
    "Strengthening exercises",
    "NDT",
    "GAIT Training",
    "Modalities + text field",
    "Breathing exercises",
    "Balance & Coordination exercises",
    "Stretching",
    "Postural correction"]
}

def generate_choices(choices):
  output = []
  count = 1
  for choice in choices.keys():
    output.append((count, choice))
    count += 1
  return output

def sub_choice_generator(choices):
  output = []
  count = 1
  for key, value in (
      itertools.chain.from_iterable(
          [itertools.product((k, ), v) for k, v in choices.items()])):
              output.append((count, value))
              count += 1
  return output
CARE_TYPES = generate_choices(CARE_CHOICES)
CARE_SUB_TYPES = sub_choice_generator(CARE_CHOICES)
class Treatment(BaseModel):
  patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True, blank=True)
  care_type = models.IntegerField(choices=CARE_TYPES, default=0)
  care_sub_type = models.IntegerField(choices=CARE_SUB_TYPES, blank=False)
  description = models.TextField(null=True, blank=False)

  def __str__(self):
    return f"{self.care_sub_type}"

class TreatmentNotes(BaseModel):
  notes = models.TextField(null=True, blank=False)
  description = models.TextField(null=True, blank=False)
  visit = models.ForeignKey(VisitSchedule, on_delete=models.PROTECT, null=True, blank=True)
  treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT, null=True, blank=True)

