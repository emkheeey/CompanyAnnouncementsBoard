import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CompanyAnnouncementsBoard.settings')
django.setup()

from announcements.models import SecureUser, SecureAnnouncement
from django.db import connection

# Create a secure user with encrypted fields
def create_secure_user():
    user = SecureUser.objects.create(
        username="johndoe",
        password="supersecret123",  # Will be stored encrypted
        email="john@example.com",  # Will be stored encrypted
        personal_info={  # Will be stored as encrypted JSON
            "address": "123 Main St",
            "phone": "555-1234",
            "department": "Engineering"
        },
        notes="This user has access to sensitive projects"  # Will be stored encrypted
    )
    print(f"Created user with ID: {user.id}")
    return user

# Create a secure announcement
def create_secure_announcement():
    announcement = SecureAnnouncement.objects.create(
        title="Confidential Project Update",
        content="The secret project X will launch next month. Please prepare all materials.",
        recipients=["engineering", "management", "marketing"]
    )
    print(f"Created announcement with ID: {announcement.id}")
    return announcement

# Retrieve and display data
def retrieve_data(user_id, announcement_id):
    # Retrieve user
    user = SecureUser.objects.get(id=user_id)
    print("\nUser data (automatically decrypted):")
    print(f"Username: {user.username}")
    print(f"Password: {user.password}")  # Automatically decrypted
    print(f"Email: {user.email}")  # Automatically decrypted
    print(f"Personal Info: {user.personal_info}")  # Automatically decrypted
    print(f"Notes: {user.notes}")  # Automatically decrypted

    # Retrieve announcement
    announcement = SecureAnnouncement.objects.get(id=announcement_id)
    print("\nAnnouncement data (automatically decrypted):")
    print(f"Title: {announcement.title}")
    print(f"Content: {announcement.content}")  # Automatically decrypted
    print(f"Recipients: {announcement.recipients}")  # Automatically decrypted

# View raw encrypted data in the database
def view_encrypted_data_in_db(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT password, email, personal_info, notes FROM announcements_secureuser WHERE id = %s",
            [user_id]
        )
        row = cursor.fetchone()
        
        print("\nRaw encrypted data in database:")
        print(f"Encrypted password: {row[0]}")
        print(f"Encrypted email: {row[1]}")
        print(f"Encrypted personal_info: {row[2]}")
        print(f"Encrypted notes: {row[3]}")

if __name__ == "__main__":
    print("Creating encrypted records...")
    user = create_secure_user()
    announcement = create_secure_announcement()
    
    print("\nRetrieving and displaying decrypted data...")
    retrieve_data(user.id, announcement.id)
    
    print("\nVerifying data is stored encrypted...")
    view_encrypted_data_in_db(user.id)
