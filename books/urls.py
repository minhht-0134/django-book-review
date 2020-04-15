from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
  path('', login_required(views.BookListView.as_view()), name='book_list'),
  path('books/', login_required(views.BookListView.as_view()), name='book_list'),
  path('books/<int:pk>/', login_required(views.BookDetailView.as_view()), name='book_detail'),
  path('activities/', login_required(views.activities)),
  path('activities/<int:pk>/change/', login_required(views.activitiesChange)),
  path('activities/<int:pk>/delete/', login_required(views.activitiesDelete)),
  path('users/<int:pk>/', login_required(views.UserDetailView.as_view()), name="user_detail"),
  path('accounts/login/', views.accountsLogin),
  path('accounts/logout/', views.accountsLogout, name='logout'),
  path('accounts/signup/', views.accountsSignup, name='signup'),
]
