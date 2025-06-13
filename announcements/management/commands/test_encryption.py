from django.core.management.base import BaseCommand
from announcements.utils.encryption import encrypt_data, decrypt_data

class Command(BaseCommand):
    help = 'Test encryption and decryption functionality'

    def add_arguments(self, parser):
        parser.add_argument('text', type=str, help='Text to encrypt and decrypt')

    def handle(self, *args, **options):
        text_to_encrypt = options['text']
        
        # Step 1: Encrypt the original text
        self.stdout.write(self.style.SUCCESS(f"Original text: {text_to_encrypt}"))
        encrypted_text = encrypt_data(text_to_encrypt)
        self.stdout.write(self.style.WARNING(f"Encrypted text: {encrypted_text}"))
        
        # Step 2: Decrypt the encrypted text
        decrypted_text = decrypt_data(encrypted_text)
        self.stdout.write(self.style.SUCCESS(f"Decrypted text: {decrypted_text}"))
        
        # Step 3: Verify that the original and decrypted texts match
        if text_to_encrypt == decrypted_text:
            self.stdout.write(self.style.SUCCESS("✅ Success! Encryption and decryption working correctly"))
        else:
            self.stdout.write(self.style.ERROR("❌ Error! Decrypted text doesn't match original"))
