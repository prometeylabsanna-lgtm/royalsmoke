from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.booking.models import Booking, BookingService, BookingSlot


class BookingSlotTests(TestCase):
    def setUp(self):
        self.service = BookingService.objects.create(
            kind=BookingService.Kind.TASTING,
            title='Tasting',
            duration_minutes=60,
            capacity=1,
        )
        start = timezone.now() + timedelta(days=1)
        self.slot = BookingSlot.objects.create(
            service=self.service,
            starts_at=start,
            ends_at=start + timedelta(hours=1),
            capacity=1,
        )

    def test_page_and_book(self):
        resp = self.client.get(reverse('booking:page'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('booking:page'), {
            'service': self.service.pk,
            'slot': self.slot.pk,
            'name': 'Ivan',
            'phone': '+380501112233',
            'email': 'i@example.com',
            'comment': '',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        # second booking should fail capacity
        resp = self.client.post(reverse('booking:page'), {
            'service': self.service.pk,
            'slot': self.slot.pk,
            'name': 'Petro',
            'phone': '+380501112244',
        })
        self.assertEqual(Booking.objects.count(), 1)
