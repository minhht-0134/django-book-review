from django.urls import path
from .views import MainPage

urlpatterns = [
    path('home/', MainPage.as_view(), name='mainpage')
]