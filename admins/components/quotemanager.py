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


class QuoteManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/quotes/index.html'
        quotes = Quote.objects.all().order_by('-updated')
        obj = {
            'current_user': current_user,
            'quotes': quotes,
        }
        return render(request, template_name, obj)


class CreateQuoteView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        author = request.POST.get('author')
        quote = Quote(
            content=content,
            author=author,
        )
        quote.save()
        
        content = f"You have created quote has author: {quote.author}"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('quote-manager')


class EditOrDeleteQuoteView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = Quote.objects.get(pk=quote_id)
        old_author = quote.author
        quote.delete()
        
        content = f"You have deleted quote has author: {old_author}"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('quote-manager')
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        content = request.POST.get('content')
        author = request.POST.get('author')
        quote = Quote.objects.get(pk=quote_id)
        quote.content = content
        quote.author = author
        quote.save()
        
        content = f"You have updated quote"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('quote-manager')
