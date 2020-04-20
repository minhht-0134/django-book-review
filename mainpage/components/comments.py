from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import *

class CommentView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        rate_id = kwargs.get('rate_id')
        content = request.POST.get('content')
        try:
            rate = Rate.objects.get(pk=rate_id)
            user = request.user
            comment = Comment(
                user=user,
                rate=rate,
                content=content
            )
            comment.save()
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)


class EditOrDeleteComment(ListView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment_id = kwargs.get('comment_id')
        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            content_data = request.POST.get('content')
            comment_id = kwargs.get('comment_id')
            comment = Comment.objects.get(pk=comment_id)
            comment.content = content_data
            comment.save()
        except:
            return redirect('book-detail', pk=pk)
        return redirect('book-detail', pk=pk)