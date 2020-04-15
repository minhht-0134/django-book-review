from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from quotes.models import Quote
from books.models import *

class MainPage(LoginRequiredMixin, ListView):
    def check_logged(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            return True, current_user
        return False, None
    
    def total_book(self):
        total = Book.objects.all().count()
        return total
    
    def get_categories(self):
        categories = Category.objects.all()
        return categories
    
    def get_books(self, request):
        books = Book.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(books, 9)
        total_page = f"{page}/{paginator.num_pages}"
        try:
            books = paginator.page(page)
        except:
            books = paginator.page(paginator.num_pages)
            total_page = f"{paginator.num_pages}/{paginator.num_pages}"
        return total_page, books
    
    def get(self, request, *args, **kwargs):
        template_name = 'mainpage/index.html'
        logged, current_user = self.check_logged(request)
        total_book = self.total_book()
        categories = self.get_categories()
        page, books = self.get_books(request)
        obj = {
            'current_user': current_user,
            'logged': logged,
            'total_book': total_book,
            'categories': categories,
            'books': books,
            'page': page
        }
        return render(request, template_name, obj)
