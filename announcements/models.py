from django.db import models
import uuid
from .utils.fields import EncryptedCharField, EncryptedTextField, EncryptedEmailField, EncryptedJsonField

class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = EncryptedTextField()  # Now using the encrypted field
    posted_by = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SecureUser(models.Model):
    username = models.CharField(max_length=100)  # Not encrypted
    password = EncryptedCharField(max_length=255)  # Encrypted
    email = EncryptedEmailField(max_length=255)  # Encrypted
    personal_info = EncryptedJsonField(null=True, blank=True)  # Encrypted JSON
    notes = EncryptedTextField(null=True, blank=True)  # Encrypted

class SecureAnnouncement(models.Model):
    title = models.CharField(max_length=200)  # Not encrypted
    content = EncryptedTextField()  # Encrypted
    recipients = EncryptedJsonField(null=True, blank=True)  # Encrypted list of recipients
    created_at = models.DateTimeField(auto_now_add=True)