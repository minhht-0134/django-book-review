from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import *
from .services import services
from .repositories import repositories

class RequestBookView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            user = request.user
            repositories.send_request_book(user, pk)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            user = request.user
            repositories.cancel_request(user, pk)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)