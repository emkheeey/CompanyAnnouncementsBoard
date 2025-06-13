from django.db import models
import uuid
from .fields import EncryptedTextField

class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = EncryptedTextField()  # Now using the encrypted field
    posted_by = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title