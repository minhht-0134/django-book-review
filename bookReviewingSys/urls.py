from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('users.urls')),
    path('', include('homepage.urls')),
    path('', include('mainpage.urls')),
]
