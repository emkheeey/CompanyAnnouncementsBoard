import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CompanyAnnouncementsBoard.settings')
django.setup()

# Import encryption utilities
from announcements.utils.encryption import encrypt_data, decrypt_data

def test_encryption():
    print("Testing Encryption and Decryption Functionality\n" + "-" * 40)
    
    # Test case 1: Simple string
    test_string = "Hello, this is a test message!"
    print("\n1. Testing with simple string:")
    encrypted = encrypt_data(test_string)
    decrypted = decrypt_data(encrypted)
    print(f"Original: {test_string}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {test_string == decrypted}")
    
    # Test case 2: Dictionary/JSON data
    test_dict = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "is_active": True
    }
    print("\n2. Testing with dictionary/JSON data:")
    encrypted = encrypt_data(test_dict)
    decrypted = decrypt_data(encrypted)
    print(f"Original: {test_dict}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {test_dict == decrypted}")
    
    # Test case 3: Number
    test_number = 12345
    print("\n3. Testing with number:")
    encrypted = encrypt_data(test_number)
    decrypted = decrypt_data(encrypted)
    print(f"Original: {test_number}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {test_number == decrypted}")
    
    # Test case 4: None/null value
    test_none = None
    print("\n4. Testing with None/null value:")
    encrypted = encrypt_data(test_none)
    decrypted = decrypt_data(encrypted)
    print(f"Original: {test_none}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {test_none == decrypted}")
    
    # Test case 5: Nested complex data
    test_complex = {
        "user": {
            "name": "Jane Smith",
            "roles": ["admin", "editor"],
            "metadata": {
                "last_login": "2023-05-15T14:30:00",
                "login_count": 42
            }
        },
        "settings": {
            "notifications": True,
            "theme": "dark"
        }
    }
    print("\n5. Testing with complex nested data:")
    encrypted = encrypt_data(test_complex)
    decrypted = decrypt_data(encrypted)
    print(f"Original: {test_complex}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {test_complex == decrypted}")

if __name__ == "__main__":
    test_encryption()
