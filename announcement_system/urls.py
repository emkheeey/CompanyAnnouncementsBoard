from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('announcements.urls')),  # Removed the 'api/' prefix
]
