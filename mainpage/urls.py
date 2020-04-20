from django.urls import path
from .views import *

urlpatterns = [
    path('home/', MainPage.as_view(), name='mainpage'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/review/', RateBookView.as_view(), name='book-review')
]