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


class CommentManagerView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        current_user = request.user
        template_name = 'admin/comments/index.html'
        list_comments = Comment.objects.all().order_by('-created')
        obj = {
            'current_user': current_user,
            'list_comments': list_comments,
        }
        return render(request, template_name, obj)


class DeleteCommentView(LoginRequiredMixin, ListView):
    
    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        comt_user = comment.user
        comt_cont = comment.content
        comment.delete()
        
        content = f"You have deleted comment of '{comt_user}': {comt_cont}"
        admin_repositories.save_action(request.user, content, 'added')
        return redirect('comment-manager')
