from django.urls import path
from .components.views import *
from .components.comments import *
from .components.favorite import *
from .components.profile import *
from .components.markbook import *
from .components.requestbook import *

urlpatterns = [
    path('home/', MainPage.as_view(), name='mainpage'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review/', RateBookView.as_view(), name='book-review'),
    path('book/<int:pk>/rate/<int:rate_id>/comment', CommentView.as_view(), name='comment-rate'),
    path('book/<int:pk>/comment/<int:comment_id>', EditOrDeleteComment.as_view(), name='edit-or-delete-comment'),
    path('book/<int:pk>/favorite', FavoriteView.as_view(), name='add-favorite'),
    path('book/<int:pk>/markread', MarkReadView.as_view(), name='mark-read'),
    path('book/<int:pk>/markreading', MarkReadingView.as_view(), name='mark-reading'),
    path('book/<int:pk>/requestbook', RequestBookView.as_view(), name='request-book'),
    path('my-profile', ProfileView.as_view(), name='profile'),
]