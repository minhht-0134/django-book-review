from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Customer
from .form import RegisterForm

after_logout = settings.LOGOUT_REDIRECT_URL

class Login(LoginView):
    template_name = "registrations/login.html"
    # extra_context = {
    #     # option 1: provide full path
    #     'next': '/account/my_custom_url/',
    #
    #     # option 2: just provide the name of the url
    #     # 'next': 'home',
    # },
    
# @login_required
class Logout(LogoutView):
    next_page = after_logout

class Register(CreateView):
    form_class = RegisterForm
    template_name = 'registrations/register.html'
    success_url = '/registration/signin/'
    