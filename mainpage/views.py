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
    
    def get_books(self, request, objects):
        page = request.GET.get('page', 1)
        paginator = Paginator(objects, 2)
        total_page = f"{page}/{paginator.num_pages}"
        try:
            objects = paginator.page(page)
        except:
            objects = paginator.page(paginator.num_pages)
            total_page = f"{paginator.num_pages}/{paginator.num_pages}"
        return total_page, objects
    
    def filter_category(self, category_id, request):
        books = Book.objects.filter(category=category_id)
        total_page, pagi = self.get_books(request, books)
        total_book = books.count()
        return total_page, pagi, total_book
    
    def get(self, request, *args, **kwargs):
        template_name = 'mainpage/index.html'
        logged, current_user = self.check_logged(request)
        books = Book.objects.all()
        book_count = self.total_book()
        categories = self.get_categories()
        category_id = request.GET.get('category')
        if category_id == "None" or category_id is None or category_id == 'all':
            page, books = self.get_books(request, books)
            total_book = book_count
            category_id = 'all'
        else:
            page, books, total_book = self.filter_category(category_id, request)
            category_id = int(category_id)

        obj = {
            'current_user': current_user,
            'logged': logged,
            'total_book': total_book,
            'book_count': book_count,
            'categories': categories,
            'books': books,
            'page': page,
            'q_category': category_id
        }
        return render(request, template_name, obj)
