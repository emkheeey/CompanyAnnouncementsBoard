from django.db import models
from django.core.exceptions import ValidationError
from .utils.encryption import encrypt_data, decrypt_data
import json

class EncryptedFieldMixin:
    """Base mixin for encrypted fields"""
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value)
        
    def to_python(self, value):
        if value is None:
            return value
        # If we get a value that was already deserialized/decrypted
        if isinstance(value, (str, int, float, bool, list, dict)):
            return value
        return decrypt_data(value)
        
    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_data(value)

class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    """Text field that automatically encrypts data"""
    description = "TextField that transparently encrypts data"
    
class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    """Char field that automatically encrypts data"""
    description = "CharField that transparently encrypts data"
    
class EncryptedEmailField(EncryptedFieldMixin, models.EmailField):
    """Email field that automatically encrypts data"""
    description = "EmailField that transparently encrypts data"
    
class EncryptedJsonField(EncryptedFieldMixin, models.TextField):
    """JSON field that automatically encrypts data"""
    description = "Field that stores JSON data encrypted"
    
    def to_python(self, value):
        # First decrypt if needed
        value = super().to_python(value)
        if value is None:
            return None
        
        # If already deserialized
        if isinstance(value, (dict, list)):
            return value
        
        # Try to deserialize
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            raise ValidationError("Invalid JSON data")
            
    def get_prep_value(self, value):
        if value is None:
            return None
            
        # Convert to JSON string first if needed
        if not isinstance(value, str):
            value = json.dumps(value)
            
        # Then encrypt
        return encrypt_data(value)
