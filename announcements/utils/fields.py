from django.db import models
from .encryption import encrypt_data, decrypt_data

class EncryptedField:
    """A mixin to create encrypted model fields"""
    
    # When saving to database, this method encrypts the data
    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            return encrypt_data(value)  # Encryption happens automatically
        return value
    
    # When reading from database, this method decrypts the data
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return decrypt_data(value)  # Decryption happens automatically
        return value

class EncryptedCharField(EncryptedField, models.CharField):
    """CharField that encrypts values before saving to database"""
    pass

class EncryptedTextField(EncryptedField, models.TextField):
    """TextField that encrypts values before saving to database"""
    pass

class EncryptedEmailField(EncryptedField, models.EmailField):
    """EmailField that encrypts values before saving to database"""
    pass

class EncryptedJsonField(EncryptedField, models.TextField):
    """Field for storing JSON data encrypted"""
    
    def get_prep_value(self, value):
        # Special handling for JSON before encryption
        import json
        if value is not None:
            return json.dumps(value)
        return value
    
    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)
        if value is not None and not isinstance(value, dict) and not isinstance(value, list):
            import json
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return value
        return value
