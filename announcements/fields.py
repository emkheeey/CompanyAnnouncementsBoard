from django.db import models
from .utils.encryption import encrypt_data, decrypt_data

class EncryptedTextField(models.TextField):
    """Custom field that automatically encrypts data before saving and decrypts when reading"""
    
    def from_db_value(self, value, expression, connection):
        # Called when data is loaded from database
        if value is None:
            return value
        return decrypt_data(value)
        
    def to_python(self, value):
        # Called when data is deserialized
        if value is None:
            return value
        # Don't decrypt if already decrypted (e.g., from form submission)
        return value if isinstance(value, str) else decrypt_data(value)
        
    def get_prep_value(self, value):
        # Called before saving to database
        if value is None:
            return value
        return encrypt_data(value)
