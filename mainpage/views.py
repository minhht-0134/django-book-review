from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from quotes.models import Quote
from books.models import *
from books.form import *

class Data():
    def getbook(self):
        print("okkkkkkkkkkkkk")
        
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
        paginator = Paginator(objects, 9)
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
        search_key = request.GET.get('search')
        search_count = None
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
            'search_key': search_key
        }
        return render(request, template_name, obj)


class BookDetailView(LoginRequiredMixin, ListView):
    def check_logged(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            return True, current_user
        return False, None
    
    def get_book(self, pk):
        book = Book.objects.get(pk=pk)
        return book
    
    def get_rate(self, book):
        # rate = Rate.objects.filter(book=book).order_by('-id')
        rate = Rate.objects.filter(book=book).order_by('-id')[:3]
        return rate
    
    def get(self, request, *args, **kwargs):
        template_name = 'bookdetail/index.html'
        logged, current_user = self.check_logged(request)
        book = self.get_book(kwargs.get('pk'))
        books = Book.objects.all()
        get_rates = self.get_rate(book)
        obj={
            'current_user': current_user,
            'logged': logged,
            'book': book,
            'books': books,
            'get_rates': get_rates
        }
        return render(request, template_name, obj)
    
class RateBookView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            book = Book.objects.get(pk=request.POST.get('book_id'))
            user = request.user
            try:
                check_rate = Rate.objects.get(user=user, book=book)
            except:
                check_rate = None
            rate_data = request.POST.get('rate')
            review_data = request.POST.get('review')
            if check_rate:
                old_rate = check_rate.score
                book.score_rate = book.score_rate - old_rate + int(rate_data)
                check_rate.score = rate_data
                check_rate.review = review_data
                check_rate.edited = True
                book.save()
                check_rate.save()
            else:
                create_rate = Rate(
                    book=book,
                    user=user,
                    score=rate_data,
                    review=review_data,
                )
                create_rate.save()
                old_score = book.score_rate
                old_total = book.total_rate
                book.score_rate = old_score + int(rate_data)
                book.total_rate = old_total +1
                book.save()

        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)
