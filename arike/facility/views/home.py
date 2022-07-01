import logging
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
  def get(self, request):
    try:
      user = self.request.user
      if user.is_active:
        role = user.role
        if role == 40:
          return redirect('arike:view-facility')
        else:
          return redirect('arike:view-patient')
      else:
        return HttpResponseRedirect('/user/login')
    except Exception as e:
      logging.error(e)
      return HttpResponseRedirect("/500")
