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


class RequestManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/requests/index.html'
        list_requests = RequestBook.objects.all().order_by('-updated')
        obj = {
            'current_user': current_user,
            'list_requests': list_requests,
        }
        return render(request, template_name, obj)
    
class ApproveRequestView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        request_id = kwargs.get('request_id')
        admin_repositories.change_status_request(request_id, 'approved', request)
        return redirect('request-manager')


class CancelRequestView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        request_id = kwargs.get('request_id')
        admin_repositories.change_status_request(request_id, 'canceled', request)
        return redirect('request-manager')


class DeleteRequestView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        request_id = kwargs.get('request_id')
        request_item = RequestBook.objects.get(pk=request_id)
        old_req = request_item.user
        request_item.delete()
        
        content = f"You have deleted request of '{old_req}'"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('request-manager')
    