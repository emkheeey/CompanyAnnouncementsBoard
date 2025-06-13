from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

# Check if ENCRYPTION_KEY exists in settings, otherwise generate one
def get_encryption_key():
    try:
        return settings.ENCRYPTION_KEY
    except AttributeError:
        # For development only - in production, this should be set in settings.py
        return os.environ.get('ENCRYPTION_KEY', 'YD-3uD9wz9aPASOdjfLi4-b9NOv4TeGK2T5iTIlHEHo=')

def encrypt_data(data):
    """Encrypt a string using Fernet symmetric encryption"""
    if not data:
        return data
        
    key = get_encryption_key()
    f = Fernet(key.encode())
    encrypted_data = f.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode()

def decrypt_data(encrypted_data):
    """Decrypt a previously encrypted string"""
    if not encrypted_data:
        return encrypted_data
        
    try:
        key = get_encryption_key()
        f = Fernet(key.encode())
        decrypted_data = f.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data.decode()
    except Exception:
        # Return original data if decryption fails
        return encrypted_data
