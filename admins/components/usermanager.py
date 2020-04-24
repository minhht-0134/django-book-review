from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import datetime
from books.models import *
from quotes.models import *
from .repositories import admin_repositories
from .services import admin_services
from .decorators import admin_required


class UserManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/users/index.html'
        list_users = User.objects.all().order_by('username')
        obj = {
            'current_user': current_user,
            'list_users': list_users,
        }
        return render(request, template_name, obj)
    
class ChangeOrDeleteUserView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        if not user.is_superuser:
            content = f"You have deleted user '{user}'"
            user.delete()
            admin_repositories.save_action(request.user, content, 'added')
        return redirect('user-manager')
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        password = request.POST.get('passw')
        passw_confirm = request.POST.get('passw_confirm')
        user = User.objects.get(pk=user_id)
        if not user.is_superuser and password == passw_confirm:
            user.set_password(password)
            user.save()
            content = f"You have changed password of user '{user}'"
            admin_repositories.save_action(request.user, content, 'added')
        return redirect('user-manager')
        