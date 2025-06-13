from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnnouncementViewSet,
    announcement_create_page,
    announcement_update_page,
    announcement_delete_page,
    AnnouncementListView,  # Keep this import
)

# Keep the router for API only
router = DefaultRouter()
router.register(r'', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Frontend page views using class-based view for list
    path('', AnnouncementListView.as_view(), name='announcement-list-page'),  # Use class-based view
    path('create/', announcement_create_page, name='announcement-create-page'),
    path('update/<uuid:id>/', announcement_update_page, name='announcement-update-page'),
    path('delete/<uuid:id>/', announcement_delete_page, name='announcement-delete-page'),
]