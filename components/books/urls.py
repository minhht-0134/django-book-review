from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryIndexView,
    CategoryUpdateView,
    CategoryDeleteView,
    BookCreateView,
    BookUpdateReadStatusView,
    BookToggleFavoriteView,
    BookIndexView,
    BookUpdateView,
    BookDeleteView,
    BookDetailView,
    CommentCreateView,
    ReviewCreateView
)

app_name = 'book'

urlpatterns = [
    path('category/create', CategoryCreateView.as_view(), name='category_create'),
    path('category', CategoryIndexView.as_view(), name='category_index'),
    path('category/<int:id>/edit', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:id>/del', CategoryDeleteView.as_view(), name='category_delete'),
    path('book/create', BookCreateView.as_view(), name='book_create'),
    path('book', BookIndexView.as_view(), name='book_index'),
    path('book/<int:id>/update-read-status', BookUpdateReadStatusView.as_view(), name='book_update_read_status'),
    path('book/<int:id>/toggle-favorite', BookToggleFavoriteView.as_view(), name='book_toggle_favorite'),
    path('book/<int:id>/edit', BookUpdateView.as_view(), name='book_update'),
    path('book/<int:id>/del', BookDeleteView.as_view(), name='book_delete'),
    path('book/<int:id>/detail', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:id>/create-comment', CommentCreateView.as_view(), name='book_create_comment'),
    path('book/<int:id>/create-review', ReviewCreateView.as_view(), name='book_create_review'),
]
