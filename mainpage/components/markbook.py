from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import *
from .services import services
from .repositories import repositories

class MarkReadView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        logged, current_user = services.check_logged(request)
        pk = kwargs.get('pk')
        repositories.mark_read_or_reading(pk, current_user, 'read')
        return redirect('book-detail', pk=pk)


class MarkReadingView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        logged, current_user = services.check_logged(request)
        pk = kwargs.get('pk')
        repositories.mark_read_or_reading(pk, current_user, 'reading')
        return redirect('book-detail', pk=pk)
    