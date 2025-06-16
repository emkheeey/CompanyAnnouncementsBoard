from django.core.management.base import BaseCommand
from django.apps import apps
from announcements.fields import EncryptedTextField, EncryptedCharField, EncryptedEmailField, EncryptedJsonField
import json
from django.db import connection

encrypted_field_types = (EncryptedTextField, EncryptedCharField, EncryptedEmailField, EncryptedJsonField)

class Command(BaseCommand):
    help = 'Demonstrate encryption/decryption in the system models'

    def handle(self, *args, **options):
        # Find models with encrypted fields
        models_with_encryption = []
        
        for model in apps.get_models():
            encrypted_fields = []
            
            for field in model._meta.fields:
                if isinstance(field, encrypted_field_types):
                    encrypted_fields.append(field.name)
            
            if encrypted_fields:
                models_with_encryption.append((model, encrypted_fields))
        
        if not models_with_encryption:
            self.stdout.write(self.style.ERROR("No models with encrypted fields found!"))
            return
            
        # Select the first model with encryption for demonstration
        model, fields = models_with_encryption[0]
        self.stdout.write(self.style.SUCCESS(f"Using model: {model.__name__}"))
        self.stdout.write(self.style.SUCCESS(f"Encrypted fields: {', '.join(fields)}"))
        
        # Create a test instance
        instance = model()
        
        # Fill in required fields to create a valid instance
        for field in model._meta.fields:
            if not field.null and not field.blank and field.name not in fields:
                if hasattr(field, 'default') and field.default:
                    # Skip if there's a default
                    continue
                
                # Basic value assignments by field type
                if field.get_internal_type() == 'CharField':
                    setattr(instance, field.name, f"Test-{field.name}")
                elif field.get_internal_type() == 'IntegerField':
                    setattr(instance, field.name, 1)
                elif field.get_internal_type() == 'BooleanField':
                    setattr(instance, field.name, True)
                # Add more types as needed
        
        # Set values for encrypted fields
        for field_name in fields:
            field = model._meta.get_field(field_name)
            if isinstance(field, EncryptedJsonField):
                test_value = {"name": "John Doe", "sensitive": "This is encrypted!"}
                setattr(instance, field_name, test_value)
            elif isinstance(field, EncryptedEmailField):
                setattr(instance, field_name, "encrypted@example.com")
            else:
                setattr(instance, field_name, f"This is encrypted text for {field_name}")
        
        # Save the instance
        instance.save()
        self.stdout.write(self.style.SUCCESS(f"Created test instance with ID: {instance.pk}"))
        
        # Display the decrypted values as seen by Django
        self.stdout.write("\nDecrypted values (as seen by the application):")
        for field_name in fields:
            value = getattr(instance, field_name)
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.stdout.write(f"  {field_name}: {value}")
        
        # Get the encrypted values directly from the database
        self.stdout.write("\nEncrypted values (as stored in database):")
        with connection.cursor() as cursor:
            table_name = model._meta.db_table
            cursor.execute(f"SELECT {', '.join(fields)} FROM {table_name} WHERE id = %s", [instance.pk])
            encrypted_values = cursor.fetchone()
            
            if encrypted_values:
                for i, field_name in enumerate(fields):
                    self.stdout.write(f"  {field_name}: {encrypted_values[i]}")
            else:
                self.stdout.write(self.style.ERROR("No data found in the database"))
