from django import forms
from arike.facility.models.patients import PatientDisease, FamilyDetail, Patient, Treatment, TreatmentNotes, VisitDetails, VisitSchedule
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, ButtonHolder, Submit, Field

class PatientForm(forms.ModelForm):
  class Meta:
    model = Patient
    fields = '__all__'
    exclude = ('deleted', 'external_id', 'created_by')
    widgets = {
        "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        "expired_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
        "address": forms.Textarea(attrs={'rows': 3}),
        "landmark": forms.Textarea(attrs={'rows': 3}),
      }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Row(
        Column('full_name', css_class="w-1/2"),
        Column('date_of_birth', css_class="w-1/2 px-2 dateinput")
      ),
      'address',
      'landmark',
      Row(
        Column('phone_number', css_class='w-1/3'),
        Column('emergency_phone_number', css_class='w-1/3 px-2'),
        Column('expired_time', css_class="w-1/3 px-2")
      ),
      Row(
        Column('ward', css_class='w-1/3'),
        Column('facility', css_class='w-1/3 px-2 disabled'),
        Column('gender', css_class='w-1/3 px-2'),
      ),
      ButtonHolder(
        Submit('submit', 'Submit', css_class='w-1/3 px-6 py-3 mt-3 text-lg text-white transition-all duration-150 ease-linear rounded-lg shadow outline-none bg-black hover:shadow-lg focus:outline-none')
      )
    )

class FamilyForm(forms.ModelForm):
  class Meta:
    model = FamilyDetail
    fields = "__all__"
    exclude = ('deleted', 'external_id')
    widgets = {
      "address": forms.Textarea(attrs={'rows': 3}),
      "occupation": forms.Textarea(attrs={'rows': 3}),
      "education": forms.Textarea(attrs={'rows': 3}),
      "remarks": forms.Textarea(attrs={'rows': 8}),
      "date_of_birth": forms.DateInput(attrs={"type": "date"}),
      "expired_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
      "is_primary": forms.CheckboxInput(),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Row(
        Column('full_name', css_class="w-2/3"),
        Column('date_of_birth', css_class='w-1/3 px-2'),
      ),
      Row(
        Column('phone_number', css_class='w-1/3'),
        Column('email', css_class='w-1/3 px-2'),
        Column('relation', css_class='w-1/3 px-2'),
      ),
      # Row(
      # ),
      'address',
      Row(
        Column('education', css_class='w-1/2'),
        Column('occupation', css_class='w-1/2 px-2'),
      ),
      Row(
        Column('remarks', css_class="w-2/3"),
        Column(
          Row('is_primary', css_class=''),
          Row('expired_time', css_class='w-2/5 px-2'),
          css_class="w-1/3 px-4 py-4"
        ),
      ),
      ButtonHolder(
        Submit('submit', 'Submit', css_class='w-1/3 px-6 py-3 mt-3 text-lg text-white transition-all duration-150 ease-linear rounded-lg shadow outline-none bg-black hover:shadow-lg focus:outline-none')
      )
    )

class DiseaseForm(forms.ModelForm):
  class Meta:
    model = PatientDisease
    fields = ["disease", "note"]
    exclude = ('deleted', 'external_id')


class TreatmentForm(forms.ModelForm):
  class Meta:
    model = Treatment
    fields = ["care_sub_type", "description"]
    exclude = ('deleted', 'external_id',)


class TreatmentNotesForm(forms.ModelForm):
  class Meta:
    model = TreatmentNotes
    fields = ["notes"]
    exclude = ('deleted', 'external_id', 'visit')

class VisitScheduleForm(forms.ModelForm):
  class Meta:
    model = VisitSchedule
    fields = "__all__"
    exclude = ('deleted', 'external_id')
    widgets = {
      "time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
    }

class VisitDetailForm(forms.ModelForm):
  class Meta:
    model = VisitDetails
    fields = "__all__"
    exclude = ('deleted', 'external_id', 'visit_schedule_id')
    widgets = {
      "patient_at_peace": forms.CheckboxInput(),
      "pain": forms.CheckboxInput(),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # self.fields['facility'].widget.attrs['readonly'] = True
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Row(
        Column('palliative_phase', css_class="w-1/2"),
        Column('blood_pressure', css_class='w-1/2 px-2'),
      ),
      Row(
        Column('pulse', css_class='w-1/3'),
        Column('general_random_blood_sugar', css_class='w-1/3 px-2'),
        Column('patient_at_peace', css_class='w-1/6 px-2'),
        Column('pain', css_class='w-1/6 px-2'),
      ),
      Row(
        Column('personal_hygiene', css_class='w-1/3'),
        Column('mouth_hygiene', css_class='w-1/3 px-2'),
        Column('pubic_hygiene', css_class='w-1/3 px-2'),
      ),
      Row(
        Column('systemic_examination', css_class='w-1/3'),
        Column('symptoms', css_class='w-2/3 px-2'),
      ),
      ButtonHolder(
        Submit('submit', 'Submit', css_class='w-1/4 px-6 py-3 -mt-10 text-lg text-white transition-all duration-150 ease-linear rounded-lg shadow outline-none bg-black hover:shadow-lg focus:outline-none')
      )
    )

