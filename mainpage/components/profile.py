from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import *
from .services import services
from .repositories import repositories

class ProfileView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'profile/index.html'
        logged, current_user = services.check_logged(request)
        actions = repositories.my_actions(current_user)
        my_favorites = repositories.my_favorites(current_user)
        read , reading = repositories.my_mark(current_user)
        list_request = repositories.list_request(current_user)
        current_admin = services.check_admin(current_user)
        obj = {
            'current_user': current_user,
            'logged': logged,
            'actions': actions,
            'my_favorites': my_favorites,
            'my_markread': read,
            'my_markreading': reading,
            'list_request': list_request,
            'current_admin': current_admin,
        }
        return render(request, template_name, obj)
    
class UserInfoView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        template_name = 'profile/index.html'
        user_id = kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        logged, current_user = services.check_logged(request)
        
        if not current_user.is_superuser and user.is_superuser:
            return redirect('profile')
        
        actions = repositories.my_actions(user)
        my_favorites = repositories.my_favorites(user)
        read , reading = repositories.my_mark(user)
        list_request = repositories.list_request(user)
        current_admin = services.check_admin(current_user)
        
        obj = {
            'username': user,
            'current_user': current_user,
            'logged': logged,
            'actions': actions,
            'my_favorites': my_favorites,
            'my_markread': read,
            'my_markreading': reading,
            'list_request': list_request,
            'current_admin': current_admin,
        }
        return render(request, template_name, obj)
    