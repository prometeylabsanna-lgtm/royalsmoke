"""Сторінка 10 «Листи і PWA»: листи, офлайн-каталог і тексти сповіщень."""

import json
from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import TestCase
from django.utils import translation
from django.utils.translation import gettext as _

from apps.core.i18n_audit import CYRILLIC
from apps.core.i18n_testing import SEA_LANGUAGES, page_strings


def _order():
    return SimpleNamespace(
        order_number='RS1',
        total='10',
        currency='USD',
        delivery_city='Kyiv',
        delivery_address='Showroom',
        get_delivery_service_display=lambda: 'Nova Poshta',
        get_payment_method_display=lambda: 'Card',
        get_status_display=lambda: 'Paid',
    )


def _booking():
    return SimpleNamespace(slot='10:00', name='An', phone='+380501112233')


class MailAndPwaTranslationTests(TestCase):
    def test_customer_emails_have_no_cyrillic(self):
        order = _order()
        booking = _booking()
        for lang in SEA_LANGUAGES:
            with translation.override(lang):
                text, html = self._render('order_created_customer', {'order': order})
                paid_text, paid_html = self._render('order_paid', {'order': order})
                book_text, _book_html = self._render('booking_created_customer', {'booking': booking})
            for body in (text, html, paid_text, paid_html, book_text):
                self.assertIsNone(CYRILLIC.search(body or ''), lang)
            phrase = page_strings(lang, '10-lysty-pwa')['Дякуємо, що обрали Royal Smoke.']
            self.assertIn(phrase, text)

    def test_offline_pack_has_every_language(self):
        html = self.client.get('/pwa/offline/').content.decode()
        start = html.index('id="rs-offline-i18n">')
        raw = html[html.index('{', start):html.index('</script>', start)]
        data = json.loads(raw)
        for lang in ('uk', 'en', 'zh-hans', *SEA_LANGUAGES):
            self.assertIn(lang, data)
            self.assertEqual(set(data[lang]), set(data['uk']))
        for lang in SEA_LANGUAGES:
            stale = page_strings(lang, '10-lysty-pwa')[
                'Офлайн-копія каталогу. Ціни та наявність можуть бути застарілими.'
            ]
            self.assertEqual(data[lang]['stale'], stale)
            self.assertIsNone(CYRILLIC.search(json.dumps(data[lang], ensure_ascii=False)))

    def test_service_worker_stale_banner_matches_the_pack(self):
        source = render_to_string('pwa/sw.js', {'admin_url': 'admin'})
        for lang in SEA_LANGUAGES:
            stale = page_strings(lang, '10-lysty-pwa')[
                'Офлайн-копія каталогу. Ціни та наявність можуть бути застарілими.'
            ]
            self.assertIn(f"'{lang}': '{stale}'", source)

    def test_push_order_texts_are_translated(self):
        for lang in SEA_LANGUAGES:
            with translation.override(lang):
                title = _('Оплату підтверджено')
                body = _('Замовлення %(num)s оплачено.') % {'num': 'RS1'}
            self.assertIsNone(CYRILLIC.search(title), lang)
            self.assertIsNone(CYRILLIC.search(body), lang)

    def test_push_permission_bar_stays_removed(self):
        source = (self._root() / 'static/js/pwa.js').read_text(encoding='utf-8')
        self.assertNotIn('rs-pwa-push-bar', source)

    def _render(self, name, context):
        from apps.core.services.notifications import render_email
        return render_email(name, context)

    def _root(self):
        from django.conf import settings
        from pathlib import Path
        return Path(settings.BASE_DIR)
