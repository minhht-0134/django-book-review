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


class RateManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/rates/index.html'
        list_rates = Rate.objects.all().order_by('-created')
        obj = {
            'current_user': current_user,
            'list_rates': list_rates,
        }
        return render(request, template_name, obj)


class DeleteRateView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        rate_id = kwargs.get('rate_id')
        rate = Rate.objects.get(pk=rate_id)
        scorerate = rate.score
        book = rate.book
        book.score_rate = book.score_rate - scorerate
        book.total_rate = book.total_rate - 1
        book.save()
        
        content = f"You have deleted rate '{book.title}' book of '{rate.user}'"
        rate.delete()
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('rate-manager')
