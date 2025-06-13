from django.db import models
import uuid
from .utils.encryption import encrypt_data, decrypt_data

class EncryptedTextField(models.TextField):
    """Custom field that automatically encrypts/decrypts data"""
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value)
        
    def to_python(self, value):
        if value is None:
            return value
        return value
        
    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_data(value)

class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)  # You could also encrypt this if needed
    message = EncryptedTextField()  # This field will be encrypted
    posted_by = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title