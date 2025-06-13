from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementListSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AnnouncementForm
from django.core.paginator import Paginator
from django.views.generic import ListView


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing announcements.
    Provides .list(), .create(), .retrieve(), .update(), and .destroy() actions.
    """
    queryset = Announcement.objects.all().order_by('-date')
    serializer_class = AnnouncementSerializer
    lookup_field = 'id'  # Ensure we use 'id' for detail views
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head']  # Exclude 'options'
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retrieve announcements from the last 7 days"""
        one_week_ago = timezone.now() - timedelta(days=7)
        recent_announcements = Announcement.objects.filter(date__gte=one_week_ago).order_by('-date')
        serializer = self.get_serializer(recent_announcements, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return AnnouncementListSerializer
        return AnnouncementSerializer

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 5
    ordering = ['-date']  # Changed from '-created_at' to '-date' to match the actual field name

def announcement_create_page(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement-list-page')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/form.html', {'form': form, 'action': 'Create'})

def announcement_update_page(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement-list-page')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/form.html', {'form': form, 'action': 'Update'})

def announcement_delete_page(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcement-list-page')
    return render(request, 'announcements/delete_confirm.html', {'announcement': announcement})
