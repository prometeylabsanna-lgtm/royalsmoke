from __future__ import annotations

import base64

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate VAPID keys for Web Push and print .env lines.'

    def handle(self, *args, **options):
        from cryptography.hazmat.primitives import serialization
        from py_vapid import Vapid01

        vapid = Vapid01()
        vapid.generate_keys()
        private_pem = vapid.private_pem().decode('utf-8').strip()
        public_raw = vapid.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
        public_b64 = base64.urlsafe_b64encode(public_raw).decode('ascii').rstrip('=')
        private_one_line = private_pem.replace('\n', '\\n')

        self.stdout.write('Add these lines to .env:\n')
        self.stdout.write(f'VAPID_PUBLIC_KEY={public_b64}')
        self.stdout.write(f'VAPID_PRIVATE_KEY={private_one_line}')
        self.stdout.write('VAPID_ADMIN_EMAIL=admin@royalsmoke.ua')
