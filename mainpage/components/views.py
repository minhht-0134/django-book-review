from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from quotes.models import Quote
from books.models import *
from books.form import *
from .services import services
from .repositories import repositories

class MainPage(LoginRequiredMixin, ListView):
    def get_books(self, request, objects):
        page = request.GET.get('page', 1)
        paginator = Paginator(objects, 6)
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
        category_id = request.GET.get('category')
        search_key = request.GET.get('search')
        search_count = None
        
        logged, current_user = services.check_logged(request)
        _, books, book_count = repositories.get_one_or_all_or_count(Book)
        _, categories, _ = repositories.get_one_or_all_or_count(Category)
        best_book = books.order_by("-score_rate")[:10]
        
        if search_key:
            books = Book.objects.filter(title__icontains=search_key)
            search_count = books.count()
        
        if category_id == "None" or category_id is None or category_id == 'all':
            page, books = self.get_books(request, books)
            total_book = book_count
            category_id = 'all'
        else:
            page, books, total_book = self.filter_category(category_id, request)
            category_id = int(category_id)

        current_admin = services.check_admin(current_user)
        obj = {
            'current_user': current_user,
            'logged': logged,
            'total_book': total_book,
            'book_count': book_count,
            'categories': categories,
            'books': books,
            'page': page,
            'q_category': category_id,
            'search_count': search_count,
            'search_key': search_key,
            'best_book': best_book,
            'current_admin': current_admin
        }
        return render(request, template_name, obj)


class BookDetailView(LoginRequiredMixin, ListView):
    def get_rate(self, book):
        rate = Rate.objects.filter(book=book).order_by('-id')[:3]
        return rate
    
    def get(self, request, *args, **kwargs):
        template_name = 'bookdetail/index.html'
        pk = kwargs.get('pk')
        
        logged, current_user = services.check_logged(request)
        book, books, _ = repositories.get_one_or_all_or_count(Book, pk)
        get_rates = self.get_rate(book)
        best_book = books.order_by("-score_rate")[:10]
        check_favorite = services.check_favorite(book, current_user)
        check_rated, rated = services.check_rated(book, current_user)
        check_read, check_reading = services.check_mark(MarkBook, book, current_user)
        request_status = services.check_request(current_user, book)
        current_admin = services.check_admin(current_user)
        obj = {
            'current_user': current_user,
            'logged': logged,
            'book': book,
            'books': books,
            'get_rates': get_rates,
            'best_book': best_book,
            'check_favorite': check_favorite,
            'check_rated': check_rated,
            'rated': rated,
            'check_read': check_read,
            'check_reading': check_reading,
            'request_status': request_status,
            'current_admin': current_admin
        }
        return render(request, template_name, obj)


class RateBookView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            book_id = request.POST.get('book_id')
            book, _, _ = repositories.get_one_or_all_or_count(Book, book_id)
            
            user = request.user
            rate_data = request.POST.get('rate')
            review_data = request.POST.get('review')
            check_rate = services.check_rate(user, book)
            if check_rate:
                repositories.have_rate(book, check_rate, rate_data, review_data)
            else:
                repositories.havent_rate(book, user, rate_data, review_data)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)
