from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import base64
import os
import json
import logging
import uuid

logger = logging.getLogger(__name__)

def get_encryption_key():
    """
    Get the encryption key from settings or environment variable.
    If not found in development, generate and store a persistent key.
    """
    # First try to get from Django settings (preferred method)
    try:
        key = settings.ENCRYPTION_KEY
        if key and _is_valid_key(key):
            return key
    except AttributeError:
        pass
    
    # Then try environment variable
    key = os.environ.get('ENCRYPTION_KEY')
    if key and _is_valid_key(key):
        return key
    
    # For development only - generate and store a key
    if settings.DEBUG:
        key_file = os.path.join(settings.BASE_DIR, '.dev_encryption_key')
        
        # Check if we already generated a key
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                key = f.read().strip()
                if _is_valid_key(key):
                    return key
        
        # Generate a new key and store it
        key = generate_key()
        try:
            with open(key_file, 'w') as f:
                f.write(key)
            logger.warning(f"Generated new encryption key for development in {key_file}")
            return key
        except Exception as e:
            logger.error(f"Failed to store generated key: {str(e)}")
    
    # No valid key found
    logger.error("No valid encryption key available. Set ENCRYPTION_KEY in settings or environment.")
    raise ValueError("Missing encryption key")

def _is_valid_key(key):
    """Check if a key is a valid Fernet key"""
    try:
        # Fernet keys must be 32 URL-safe base64-encoded bytes
        key_bytes = base64.urlsafe_b64decode(key.encode())
        return len(key_bytes) == 32
    except Exception:
        return False

def generate_key():
    """Generate a new Fernet key for encryption"""
    return Fernet.generate_key().decode()

def encrypt_data(data):
    """Encrypt data using Fernet symmetric encryption
    
    Handles different data types by converting to JSON string first
    """
    if data is None:
        return None
        
    # Convert non-string data to JSON string
    if not isinstance(data, str):
        data = json.dumps(data)
        
    key = get_encryption_key()  # Get the encryption key
    f = Fernet(key.encode())    # Create a cipher with the key
    encrypted_data = f.encrypt(data.encode())  # Use the key to encrypt
    return base64.b64encode(encrypted_data).decode()

def decrypt_data(encrypted_data):
    """Decrypt a previously encrypted string"""
    if not encrypted_data:
        return encrypted_data
        
    try:
        key = get_encryption_key()  # Get the same key
        f = Fernet(key.encode())    # Create a cipher with the key
        decrypted_data = f.decrypt(base64.b64decode(encrypted_data))  # Use the key to decrypt
        data = decrypted_data.decode()
        
        # Try to parse as JSON in case it was a serialized object
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            # If not valid JSON, return as string
            return data
    except InvalidToken:
        logger.error(f"Failed to decrypt data: invalid token")
        return None
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return None