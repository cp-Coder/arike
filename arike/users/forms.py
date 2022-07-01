from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, ButtonHolder, Submit
from arike.facility.models.facility import FacilityUser


User = get_user_model()
class RegistrationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ["full_name", "email", "role", "phone"]

  def clean_email(self):
    email = self.cleaned_data.get('email')
    model_obj = User.objects.filter(email=email)
    if model_obj.exists():
      raise forms.ValidationError("email is taken")
    return email

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    password_2 = cleaned_data.get("password_2")
    if password is not None and password != password_2:
      self.add_error("password_2", "Your passwords must match")
    return cleaned_data

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password"])
    if commit:
      user.save()
    return user


class UserAdminCreationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['email']

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    password_2 = cleaned_data.get("password_2")
    if password is not None and password != password_2:
        self.add_error("password_2", "Your passwords must match")
    return cleaned_data

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password"])
    if commit:
      user.save()
    return user


class UserAssignForm(forms.ModelForm):
  class Meta:
    model = FacilityUser
    fields = ["user", "facility"]

class UserAdminChangeForm(forms.ModelForm):
  password = ReadOnlyPasswordHashField()

  class Meta:
    model = User
    fields = ['email', 'password', 'is_active', 'admin']

  def clean_password(self):
    return self.initial["password"]
class UserAuthenticationForm(forms.ModelForm):
  password = forms.CharField(label='Password', widget=forms.PasswordInput)
  class Meta:
    model = User
    fields = ['email', 'password']

  def clean(self):
    if self.is_valid():
      email = self.cleaned_data['email']
      password = self.cleaned_data['password']
      if not authenticate(email=email, password=password):
        raise forms.ValidationError("Invalid login")


class UserAdminUpdateForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_1 = forms.CharField(widget=forms.PasswordInput)
  password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
  class Meta:
    model = User
    fields = ["full_name", "email", "phone"]

  def clean_email(self):
    email = self.cleaned_data['email']
    password = self.cleaned_data['password']
    try:
      user = User.objects.exclude(pk=self.instance.pk).get(email=email)
    except user.DoesNotExist:
      return email
    if not authenticate(email=email, password=password):
      raise forms.ValidationError("Invalid login")
    raise forms.ValidationError('Email "%s" is already in use.' % user)

  def clean_password(self):
    password_1 = self.cleaned_data['password_1']
    password_2 = self.cleaned_data['password_2']

    if password_1 is not None and password_1 != password_2:
        self.add_error("password_2", "Your passwords must match")

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password_1"])
    if commit:
      user.save()
    return user



class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["full_name", "role", "phone"]

  # def clean_email(self):
  #   email = self.cleaned_data['email']
  #   try:
  #     user = User.objects.exclude(pk=self.instance.pk).get(email=email)
  #   except user.DoesNotExist:
  #     return email
  #   raise forms.ValidationError('Email "%s" is already in use.' % user)

# class UserSearchForm(forms.ModelForm):
#   class Meta:
#     model = User
#     fields = ["role"]
#     exclude = ['external_id']

#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields['role'].widget.attrs['required'] = False
#     self.helper = FormHelper()
#     self.helper.layout = Layout(
#       Row(
#         Column('role', css_class='w-1/5 pl-40'),
#         Column('facility', css_class='w-1/5 ml-10 pr-40'),
#         # Column('kind', css_class="w-1/5 pl-40"),
#         ButtonHolder(
#           Submit('submit', 'Filter', css_class='w-1/5 px-16 py-2 ml-10 mt-8 text-md text-white rounded-lg outline-none bg-black hover:shadow-lg focus:outline-none')
#         ), css_class="mt-10 flex flex-row"
#       )
#     )
