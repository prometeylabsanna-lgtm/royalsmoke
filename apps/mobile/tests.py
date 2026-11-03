from django.test import Client, TestCase

from apps.mobile.language import normalize_lang, resolve_mobile_language
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

    def test_lang_query_and_accept_language(self):
        brand = MobileBrand.objects.get(slug='aj')
        brand.heritage_uk = 'Українська спадщина'
        brand.heritage_en = 'English heritage'
        brand.heritage_zh_hans = '中文传承'
        brand.heritage_ind = 'Warisan Indonesia'
        brand.save()
        screen = MobileScreen.objects.get(key='home')
        screen.title_uk = 'Дім UA'
        screen.title_en = 'Home EN'
        screen.title_vi = 'Nhà VI'
        screen.save()

        en = self.client.get('/api/v1/app/bundle/?lang=en')
        self.assertEqual(en.status_code, 200)
        self.assertEqual(en['Content-Language'], 'en')
        self.assertEqual(en.json()['brands'][0]['heritage'], 'English heritage')
        self.assertEqual(en.json()['screens']['home']['title'], 'Home EN')

        uk = self.client.get('/api/v1/app/bundle/?lang=uk', HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(uk.json()['brands'][0]['heritage'], 'Українська спадщина')
        self.assertEqual(uk['Content-Language'], 'uk')

        zh = self.client.get('/api/v1/app/brands/aj/?lang=zh_Hans')
        self.assertEqual(zh.json()['heritage'], '中文传承')

        ind = self.client.get('/api/v1/app/bundle/', HTTP_ACCEPT_LANGUAGE='id-ID,id;q=0.9')
        self.assertEqual(ind.json()['brands'][0]['heritage'], 'Warisan Indonesia')
        self.assertEqual(ind['Content-Language'], 'id')

        vi = self.client.get('/api/v1/app/screens/home/?lang=vi')
        self.assertEqual(vi.json()['title'], 'Nhà VI')

        unknown = self.client.get('/api/v1/app/bundle/?lang=de')
        self.assertEqual(unknown['Content-Language'], 'uk')
        self.assertEqual(unknown.json()['screens']['home']['title'], 'Дім UA')

        header = self.client.get('/api/v1/app/settings/', HTTP_ACCEPT_LANGUAGE='fr,en;q=0.8')
        self.assertEqual(header['Content-Language'], 'en')

    def test_language_resolver(self):
        self.assertEqual(normalize_lang('zh_CN'), 'zh-hans')
        self.assertIsNone(normalize_lang('zh-Hant'))
        self.assertEqual(normalize_lang('fil-PH'), 'fil')

        class _Req:
            GET = {}
            META = {'HTTP_ACCEPT_LANGUAGE': 'de, vi-VN;q=0.5'}

        self.assertEqual(resolve_mobile_language(_Req()), 'vi')

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
