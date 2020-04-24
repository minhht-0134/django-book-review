from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    
    path('admin/', admin.site.urls),
    path('registration/', include('users.urls')),
    path('', include('homepage.urls')),
    path('', include('mainpage.urls')),
    path('managements/', include('admins.urls')),
]
# if settings.DEBUG:
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
