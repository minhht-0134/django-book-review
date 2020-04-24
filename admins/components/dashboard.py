from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from books.models import *
from quotes.models import *
from .repositories import admin_repositories
from .services import admin_services
from .decorators import admin_required

class DashboardView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/dashboard/index.html'
        count_books = admin_repositories.count_model(Book)
        count_categories = admin_repositories.count_model(Category)
        count_users = admin_repositories.count_model(User, 'user')
        count_comments = admin_repositories.count_model(Comment)
        count_request = admin_repositories.count_model(RequestBook)
        count_quotes = admin_repositories.count_model(Quote)
        count_rates = admin_repositories.count_model(Rate)
        top_favorite = admin_repositories.top_favorite()
        top_read = admin_repositories.top_mark('read')
        top_reading = admin_repositories.top_mark('reading')
        top_rate = admin_repositories.top_rate()
        
        obj = {
            'current_user': current_user,
            'count_books': count_books,
            'count_categories': count_categories,
            'count_users': count_users,
            'count_comments': count_comments,
            'count_request': count_request,
            'count_quotes': count_quotes,
            'count_rates': count_rates,
            'top_favorite': top_favorite,
            'top_rate': top_rate,
            'top_read': top_read,
            'top_reading': top_reading,
        }
        return render(request, template_name, obj)
    