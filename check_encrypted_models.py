import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CompanyAnnouncementsBoard.settings')
django.setup()

from django.apps import apps
from announcements.fields import EncryptedTextField, EncryptedCharField, EncryptedEmailField, EncryptedJsonField

encrypted_field_types = (EncryptedTextField, EncryptedCharField, EncryptedEmailField, EncryptedJsonField)

print("Models with encrypted fields:")
print("-" * 50)

for model in apps.get_models():
    encrypted_fields = []
    
    for field in model._meta.fields:
        if isinstance(field, encrypted_field_types):
            encrypted_fields.append(field.name)
    
    if encrypted_fields:
        print(f"\nModel: {model.__name__}")
        print(f"App: {model._meta.app_label}")
        print(f"Encrypted fields: {', '.join(encrypted_fields)}")
