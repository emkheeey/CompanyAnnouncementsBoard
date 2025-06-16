from django.core.management.base import BaseCommand
from announcements.utils.encryption import generate_key

class Command(BaseCommand):
    help = 'Generate a new encryption key for the application'

    def handle(self, *args, **options):
        key = generate_key()
        self.stdout.write(self.style.SUCCESS(f"Generated new encryption key:"))
        self.stdout.write(self.style.WARNING(f"{key}"))
        self.stdout.write(self.style.SUCCESS("Add this key to your settings.py:"))
        self.stdout.write(self.style.SUCCESS("ENCRYPTION_KEY = 'your-key-here'"))
        self.stdout.write(self.style.SUCCESS("Or set as environment variable:"))
        self.stdout.write(self.style.SUCCESS("export ENCRYPTION_KEY='your-key-here'"))
