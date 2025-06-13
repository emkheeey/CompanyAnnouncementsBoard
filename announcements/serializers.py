from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'message', 'posted_by', 'date']
        read_only_fields = ['id', 'date']

class AnnouncementListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'message', 'posted_by', 'date']