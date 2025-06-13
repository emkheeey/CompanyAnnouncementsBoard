import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Announcement

class AnnouncementModelTest(TestCase):
    def test_announcement_creation(self):
        announcement = Announcement.objects.create(
            title="Test Announcement",
            message="Test message",
            posted_by="Test User"
        )
        self.assertTrue(isinstance(announcement.id, uuid.UUID))
        self.assertEqual(str(announcement), "Test Announcement")

class AnnouncementAPITest(APITestCase):
    def setUp(self):
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            message="Test message",
            posted_by="Test User"
        )
    
    def test_get_announcements(self):
        url = reverse('announcement-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_announcement(self):
        url = reverse('announcement-list-create')
        data = {
            'title': 'New Announcement',
            'message': 'New message',
            'posted_by': 'New User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_announcement_detail(self):
        url = reverse('announcement-detail', kwargs={'id': self.announcement.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_announcement(self):
        url = reverse('announcement-detail', kwargs={'id': self.announcement.id})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_announcement(self):
        url = reverse('announcement-detail', kwargs={'id': self.announcement.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)