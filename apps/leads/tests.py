from django.test import TestCase
from django.urls import reverse

from apps.leads.models import Lead


class LeadFormTests(TestCase):
    def test_callback_creates_lead(self):
        resp = self.client.post(reverse('leads:callback'), {
            'name': 'Ivan',
            'phone': '+380501112233',
        }, HTTP_REFERER='/')
        self.assertEqual(resp.status_code, 302)
        lead = Lead.objects.get()
        self.assertEqual(lead.kind, Lead.Kind.CALLBACK)
        self.assertEqual(lead.phone, '+380501112233')

    def test_callback_invalid_sets_error(self):
        resp = self.client.post(reverse('leads:callback'), {
            'name': 'Ivan',
            'phone': '12',
        }, HTTP_REFERER='/service/contact/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Lead.objects.count(), 0)

    def test_contact_requires_phone_or_email(self):
        resp = self.client.post(reverse('leads:contact'), {
            'name': 'Ivan',
            'message': 'Hello there',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_contact_creates_lead(self):
        resp = self.client.post(reverse('leads:contact'), {
            'name': 'Ivan',
            'phone': '+380501112233',
            'email': '',
            'message': 'Need a humidor',
        })
        self.assertEqual(resp.status_code, 302)
        lead = Lead.objects.get()
        self.assertEqual(lead.kind, Lead.Kind.CONTACT)
        self.assertEqual(lead.message, 'Need a humidor')

    def test_b2b_get_redirects_to_home_block(self):
        resp = self.client.get(reverse('leads:b2b'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/#home-b2b')
