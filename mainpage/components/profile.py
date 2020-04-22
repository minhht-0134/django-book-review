from django.shortcuts import render
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
        obj = {
            'current_user': current_user,
            'logged': logged,
            'actions': actions,
            'my_favorites': my_favorites,
            'my_markread': read,
            'my_markreading': reading,
            'list_request': list_request,
        }
        return render(request, template_name, obj)
    