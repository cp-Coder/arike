import logging
from django.template import Library
from arike.facility.models.patients import RELATION_CHOICES, CARE_SUB_TYPES, SYSTEMIC_EXAMINATION

register = Library()

@register.filter(name="get_profession")
def get_profession(role):
  if role == 10:
    return "Primary Nurse"
  elif role == 5:
    return "Secondary Nurse"

@register.filter(name="get_name")
def get_name(dict, key):
  return dict.get(key)

@register.filter(name="facility_type")
def facility_type(kind):
  if kind == 1:
    return "PHC"
  else:
    return "CHC"


@register.filter(name="relation_type")
def relation_type(choice):
  return RELATION_CHOICES[choice - 1][1]

@register.filter(name="care_sub_type")
def care_sub_type(choice):
  return CARE_SUB_TYPES[choice - 1][1]

@register.filter(name="get_gender")
def get_gender(choice):
  if choice == 1:
    return "Male"
  elif choice == 2:
    return "Female"
  return "Non-binary"

@register.filter(name="get_systemic_examination")
def get_systemic_examination(choice):
  return SYSTEMIC_EXAMINATION[choice - 1][1]
