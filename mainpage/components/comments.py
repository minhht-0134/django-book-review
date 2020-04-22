from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import *
from .services import services
from .repositories import repositories

class CommentView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            rate_id = kwargs.get('rate_id')
            content = request.POST.get('content')
            user = request.user
            repositories.create_comment(rate_id, content, user)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)


class EditOrDeleteComment(ListView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            comment_id = kwargs.get('comment_id')
            user = request.user
            repositories.delete_comment(comment_id, user)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            user = request.user
            content_data = request.POST.get('content')
            comment_id = kwargs.get('comment_id')
            repositories.edit_comment(comment_id, user, content_data)
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)