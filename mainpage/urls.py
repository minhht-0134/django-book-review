from django.urls import path
from .components.views import *
from .components.comments import *

urlpatterns = [
    path('home/', MainPage.as_view(), name='mainpage'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review/', RateBookView.as_view(), name='book-review'),
    path('book/<int:pk>/rate/<int:rate_id>/comment', CommentView.as_view(), name='comment-rate'),
    path('book/<int:pk>/comment/<int:comment_id>', EditOrDeleteComment.as_view(), name='edit-or-delete-comment')
]