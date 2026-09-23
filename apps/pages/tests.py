from django.test import TestCase
from django.urls import reverse

CREDIT_URL = 'https://www.prometeylabs.com/internet-shop-v2/'


class FooterDeveloperLinkTests(TestCase):
    def test_home_has_nofollow_credit_link(self):
        response = self.client.get(reverse('pages:home'))
        self.assertContains(response, CREDIT_URL)
        self.assertContains(response, 'nofollow')
        self.assertContains(response, 'rs-footer__credit-link')
        self.assertContains(response, '>PrometeyLabs</a>')

    def test_localized_home_keeps_credit_link(self):
        for path in ('/en/', '/zh-hans/'):
            response = self.client.get(path)
            self.assertContains(response, CREDIT_URL, msg_prefix=path)
            self.assertContains(response, 'nofollow', msg_prefix=path)
            self.assertContains(response, '>PrometeyLabs</a>', msg_prefix=path)

    def test_inner_pages_show_credit_without_link(self):
        urls = (
            reverse('pages:about'),
            reverse('catalog:list'),
            reverse('pages:faq'),
        )
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'PrometeyLabs', msg_prefix=url)
            self.assertNotContains(response, CREDIT_URL, msg_prefix=url)
            self.assertNotContains(response, 'rs-footer__credit-link', msg_prefix=url)
            self.assertContains(response, 'rs-footer__credit-name', msg_prefix=url)
