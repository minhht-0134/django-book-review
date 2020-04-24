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


class BookManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/books/index.html'
        books = Book.objects.all().order_by('-updated')
        categories = Category.objects.all()
        obj = {
            'current_user': current_user,
            'books': books,
            'categories': categories,
        }
        return render(request, template_name, obj)
    
class CreateBookView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        user = request.user
        title = request.POST.get('title')
        author = request.POST.get('author')
        pages = request.POST.get('pages')
        category = Category.objects.get(pk=request.POST.get('category'))
        book_url = request.POST.get('book_url')
        image_url = request.POST.get('image_url')
        publish_date = request.POST.get('publish_date')
        convert_publish = datetime.datetime.now()
        if publish_date:
            convert_publish = datetime.datetime.strptime(publish_date, '%d/%m/%Y')
        book = Book(
            title=title,
            author=author,
            pages=pages,
            category=category,
            book_url=book_url,
            image_url=image_url,
            publish_date=convert_publish,
        )
        book.save()
        content = f"You have created '{title}' book"
        admin_repositories.save_action(user, content, 'added')
        return redirect('book-manager')
    
class EditOrDeleteBookView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')
        book = Book.objects.get(pk=pk)
        old_book = book.title
        book.delete()
        
        content = f"You have deleted '{old_book}' book"
        admin_repositories.save_action(user, content, 'edited')
        return redirect('book-manager')
    
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user
        title = request.POST.get('title')
        author = request.POST.get('author')
        pages = request.POST.get('pages')
        category = Category.objects.get(pk=request.POST.get('categoryselected'))
        book_url = request.POST.get('book_url')
        image_url = request.POST.get('image_url')
        publish_date = request.POST.get('publish_date')
        convert_publish = datetime.datetime.now()
        if publish_date:
            convert_publish = datetime.datetime.strptime(publish_date, '%d/%m/%Y')
        book = Book.objects.get(pk=pk)
        old_book = book.title
        book.title = title
        book.author = author
        book.pages = pages
        book.category = category
        book.book_url = book_url
        book.image_url = image_url
        book.convert_publish = convert_publish
        book.save()
        
        content = f"You have updated '{old_book}' book to '{book.title}'"
        admin_repositories.save_action(user, content, 'edited')
        return redirect('book-manager')
