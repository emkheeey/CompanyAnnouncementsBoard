from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnnouncementViewSet,
    announcement_create_page,
    announcement_update_page,
    announcement_delete_page,
    AnnouncementListView,
)

# Keep the router but use a more specific URL pattern
router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    # API endpoints with distinct URL pattern
    path('api/', include(router.urls)),
    
    # Frontend page views
    path('', AnnouncementListView.as_view(), name='announcement-list-page'),
    path('create/', announcement_create_page, name='announcement-create-page'),
    path('detail/<uuid:id>/', announcement_update_page, name='announcement_detail'),  # Added detail URL with underscore name
    path('update/<uuid:id>/', announcement_update_page, name='announcement-update-page'),
    path('delete/<uuid:id>/', announcement_delete_page, name='announcement-delete-page'),
]