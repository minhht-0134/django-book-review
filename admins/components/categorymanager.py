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


class CategoryManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/categories/index.html'
        categories = Category.objects.all().order_by('-updated')
        obj = {
            'current_user': current_user,
            'categories': categories,
        }
        return render(request, template_name, obj)


class CreateCategoryView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        category = Category(
            name=name,
        )
        category.save()
        
        content = f"You have created '{category.name}' category"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('category-manager')


class EditOrDeleteCategoryView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = Category.objects.get(pk=category_id)
        old_cate = category.name
        category.delete()
        
        content = f"You have deleted '{old_cate}' category"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('category-manager')
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        name = request.POST.get('name')
        category = Category.objects.get(pk=category_id)
        old_cate = category.name
        category.name = name
        category.save()
        content = f"You have updated '{old_cate}' to '{category.name}' category"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('category-manager')
