import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, authenticate, update_session_auth_hash
from arike.users.forms import RegistrationForm, UserAdminUpdateForm, UserAssignForm, UserAuthenticationForm, UserUpdateForm
from arike.users.models import User
from arike.facility.models.facility import FacilityUser
from arike.facility.models.facility import Facility

class AuthView(View):
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return HttpResponseRedirect('/user/login')
    if request.user.role != 40:
      return HttpResponseRedirect("/403")
    return super().dispatch(request, *args, **kwargs)

  # will give all the wards available in that particular district
  def choices(self, request):
    return Facility.objects.filter(ward__lsg_body__district__name__icontains=request.user.district, deleted=False)

class LoginView(View):
  model = User
  form_class = UserAuthenticationForm
  template = "users/login.html"

  def get(self, request):
    try:
      user = self.request.user
      if user.is_authenticated:
        if user.role >= 40:
          return redirect("/facility/view")
        else:
          return redirect("/patient/view")
      form = self.form_class()
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request):
    try:
      data = self.request.POST
      form = self.form_class(data)
      if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
          login(request, user)
        if user.role >= 40:
          return redirect("/facility/view")
        else:
          return redirect("/patient/view")
      else:
        return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")


# class ProfileView(View):
#   form_class = UserAdminUpdateForm
#   template = "users/update.html"

#   def get(self, request):
#     try:
#       if not request.user.is_authenticated:
#         return HttpResponseRedirect('/user/login')
#       form = self.form_class(initial={
#         "email": request.user.email,
#         "full_name": request.user.full_name
#       })
#       # form.fields["email"].widget.attrs["disabled"] ="disabled"
#       return render(request, self.template, {"form": form})
#     except Exception as e:
#       logging.error(e)
#       return HttpResponseRedirect("/500")

#   def post(self, request):
#     try:
#       # breakpoint()
#       data = request.POST
#       form = self.form_class(data)
#       if form.is_valid():
#         form.save()
#         return redirect("user:profile")
#       # form.fields["email"].widget.attrs["disabled"] ="disabled"
#       return render(request, self.template, {"form": form})
#     except Exception as e:
#         logging.error(e)
#         return HttpResponseRedirect("/500")


class CreateUser(AuthView):
  model = User
  template = "users/create.html"
  form_class = RegistrationForm

  def get(self, request):
    try:
      form = self.form_class()
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
        model_obj.district = request.user.district
        model_obj.save()
        return redirect("user:view-user")
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class UpdateUser(AuthView):
  model = User
  template = "users/update.html"
  form_class = UserUpdateForm

  def get(self, request, pk):
    try:
      model_obj = self.model.objects.get(id=pk, district=request.user.district)
      form = self.form_class(instance=model_obj)
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
        return redirect("user:view-user")
      form.fields["email"].widget.attrs["disable"] = "disabled"
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class AssignFacilityUser(AuthView):
  model = FacilityUser
  template = "users/assign.html"
  form_class = UserAssignForm

  def get(self, request, pk):
    try:
      form = self.form_class()
      form.fields["user"].queryset = User.objects.filter(id=pk)
      form.fields["facility"].queryset = Facility.objects.filter(created_by=request.user)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk):
    try:
      current_user = request.user
      data = request.POST
      form = self.form_class(data)
      if form.is_valid():
        model_obj = form.save(commit=False)
        # model_obj.user
        model_obj.created_by = current_user
        model_obj.save()
        return redirect("user:view-user")
      form.fields["user"].queryset = User.objects.filter(id=pk)
      form.fields["facility"].queryset = Facility.objects.filter(created_by=request.user)
      return render(request, self.template, {"form": form})
    except Exception as e:
        logging.error(e)
        return HttpResponseRedirect("/500")

class ChangeFacilityUser(AuthView):
  model = FacilityUser
  template = "users/update.html"
  form_class = UserAssignForm

  def get(self, request, pk):
    try:
      current_user = request.user
      model_obj = self.model.objects.get(id=pk, created_by=current_user)
      form = self.form_class(instance=model_obj)
      form.fields["user"].queryset = User.objects.filter(id=pk)
      form.fields["facility"].queryset = Facility.objects.filter(created_by=request.user)
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
        return redirect("user:view-user")
      form.fields["user"].queryset = User.objects.filter(id=pk)
      form.fields["facility"].queryset = Facility.objects.filter(created_by=request.user)
      return render(request, self.template, {"form": form})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class ViewUser(AuthView):
  model = User
  template = "users/view.html"

  def get(self, request):
    try:
      data = self.model.objects.exclude(email=request.user.email).filter(deleted=False, district__name=request.user.district)
      facility = {}
      for dt in data:
        try:
          fac_id = FacilityUser.objects.get(user_id=dt.id).facility_id
          if fac_id:
            facility[dt.id] = Facility.objects.get(id=fac_id).name
        except:
          pass
      return render(request, self.template, {"data": data, "facility": facility})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DetailUser(AuthView):
  model = User
  template = "users/detail.html"

  def get(self, request, pk):
    try:
      data = self.model.objects.get(id=pk)
      return render(request, self.template, {"data": data})
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

class DeleteUser(AuthView):
  model = User
  template = "facility/delete.html"

  def get(self, request, pk):
    try:
      data = User.objects.get(id=pk, district__name=request.user.district).full_name
      return render(request, self.template, {"data": data})
      return HttpResponseRedirect("/404")
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")

  def post(self, request, pk):
    try:
      res = request.POST.get("confirm_delete")
      if res == "yes":
        model_obj = self.model.objects.get(pk=pk)
        model_obj.delete()
      return redirect("user:view-user")
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")


class ChangePassword(PasswordChangeView):
  template_name = "users/update.html"
  success_url = "/"
