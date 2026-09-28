from django.test import Client, TestCase

from apps.mobile.models import MobileBrand, MobileLegalPage, MobileScreen, MobileSettings


class MobileAppApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        MobileSettings.load()
        MobileBrand.objects.create(
            slug='aj',
            name='AJ Fernandez',
            short_name='AJ',
            mono='AJ',
            country='Нікарагуа',
            panel='amber',
            heritage='Test heritage',
            sort_order=0,
        )
        MobileScreen.objects.create(key='home', title='ROYAL SMOKE', body='Довідник')
        MobileLegalPage.objects.create(slug='about', title='Про застосунок', body='Текст')

    def test_bundle(self):
        r = self.client.get('/api/v1/app/bundle/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('settings', data)
        self.assertEqual(len(data['brands']), 1)
        self.assertEqual(data['brands'][0]['id'], 'aj')
        self.assertIn('home', data['screens'])
        self.assertIn('about', data['pages'])

    def test_brands_list(self):
        r = self.client.get('/api/v1/app/brands/')
        self.assertEqual(r.status_code, 200)
        payload = r.json()
        items = payload['results'] if isinstance(payload, dict) and 'results' in payload else payload
        self.assertEqual(items[0]['slug'], 'aj')

    def test_settings(self):
        r = self.client.get('/api/v1/app/settings/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('contact_lat', r.json())

    def test_admin_changelist(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_superuser(email='admin@test.ua', password='pass12345')
        self.client.force_login(user)
        for path in (
            '/rs-admin/mobile/mobilesettings/',
            '/rs-admin/mobile/mobilebrand/',
            '/rs-admin/mobile/mobilescreen/',
            '/rs-admin/mobile/mobilelegalpage/',
        ):
            r = self.client.get(path)
            self.assertEqual(r.status_code, 200, path)
