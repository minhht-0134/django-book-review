from django.urls import path, include
from .views import *

urlpatterns = [
    path('signin/', Login.as_view(), name='signin'),
    path('signout/', Logout.as_view(), name='signout'),
    path('signup/', Register.as_view(), name='signup'),
]
