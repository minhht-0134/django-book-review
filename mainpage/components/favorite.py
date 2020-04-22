from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import *
from .services import services
from .repositories import repositories

class FavoriteView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book = Book.objects.get(pk=pk)
        user = request.user
        repositories.add_favorite(user, book)
        return redirect('book-detail', pk=pk)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book = Book.objects.get(pk=pk)
        user = request.user
        try:
            repositories.remove_favorite(user, book)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)