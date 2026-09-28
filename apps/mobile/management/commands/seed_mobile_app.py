from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.mobile.models import (
    MobileBrand,
    MobileBrandFact,
    MobileBrandLine,
    MobileHouseBlock,
    MobileLegalPage,
    MobileScreen,
    MobileSettings,
)

MOBILE_ROOT = Path(settings.BASE_DIR) / 'mobile' / 'assets' / 'images'

BRANDS = [
    {
        'slug': 'aj',
        'mono': 'AJ',
        'short_name': 'AJ',
        'name': 'AJ Fernandez',
        'country': 'Нікарагуа',
        'panel': 'amber',
        'cover': 'brands/aj.jpg',
        'heritage': (
            'Абдель Фернандес — представник четвертого покоління кубинської родини майстрів. '
            'Власну мануфактуру в Естелі заснував на початку 2000-х; компанія розвиває '
            'виробництво в кількох регіонах Нікарагуа.'
        ),
        'facts': [
            ('Походження', 'Естелі, Нікарагуа'),
            ('Засновано', 'Початок 2000-х'),
            ('Родина', 'Фернандес, кубинське коріння'),
            ('Характер ліній', 'Насичені, виразні профілі'),
        ],
        'lines': ['New World', 'Bellas Artes', 'Enclave', 'San Lotano'],
    },
    {
        'slug': 'oliva',
        'mono': 'O',
        'short_name': 'Oliva',
        'name': 'Oliva',
        'country': 'Нікарагуа',
        'panel': 'burgundy',
        'cover': 'brands/oliva.jpg',
        'heritage': (
            'Родина Олива розвиває свою справу з кінця XIX століття, починаючи з провінції '
            'Пінар-дель-Ріо на Кубі. Після еміграції виробництво зосередилося в Нікарагуа, '
            'де розташовані основні майстерні та фабрика бренду.'
        ),
        'facts': [
            ('Походження', 'Естелі, Нікарагуа'),
            ('Традиція', 'З кінця XIX ст., Куба'),
            ('Виробництво', 'Власні майстерні в долині Хамастран'),
            ('Характер ліній', 'Від збалансованих до насичених'),
        ],
        'lines': ['Serie V', 'Serie G', 'Master Blends', 'Serie O'],
    },
    {
        'slug': 'perdomo',
        'mono': 'P',
        'short_name': 'Perdomo',
        'name': 'Perdomo',
        'country': 'Нікарагуа',
        'panel': 'green',
        'cover': 'brands/perdomo.jpg',
        'heritage': (
            'Бренд засновано в Маямі на початку 1990-х. Згодом виробництво перенесено до Естелі, '
            'де компанія вибудувала повний цикл — від власних ділянок до фабрики та тривалої витримки.'
        ),
        'facts': [
            ('Походження', 'Естелі, Нікарагуа'),
            ('Засновано', '1990-ті, Маямі'),
            ('Засновник', 'Нік Пердомо'),
            ('Особливість', 'Тривала витримка матеріалів'),
        ],
        'lines': ['Reserve 10th Anniversary', 'Habano', 'Lot 23'],
    },
    {
        'slug': 'turrent',
        'mono': 'CT',
        'short_name': 'Casa Turrent',
        'name': 'Casa Turrent',
        'country': 'Мексика',
        'panel': 'brown',
        'cover': 'brands/turrent.jpg',
        'heritage': (
            'Мексиканський бренд родини Турренте. Виробництво в долині Сан-Андрес, штат Веракрус; '
            'глибокі місцеві традиції та характерний стиль регіону.'
        ),
        'facts': [
            ('Походження', 'Сан-Андрес, Мексика'),
            ('Родина', 'Турренте'),
            ('Характер ліній', 'Насичений профіль, стійкий фініш'),
        ],
        'lines': ['1942', '1880', 'Origin Series', 'Serie 1901'],
    },
]

SCREENS = {
    'splash': {
        'kicker': 'ДОВІДНИК БРЕНДУ',
        'title': 'ROYAL SMOKE',
        'cta_primary': 'ВІДКРИТИ',
    },
    'age': {
        'kicker': 'Підтвердження віку · 21+',
        'title': 'Лише для повнолітніх',
        'body': (
            'Застосунок є інформаційним довідником брендів. Вміст призначений виключно '
            'для осіб, яким виповнилося 21 рік.'
        ),
        'legal_note': (
            'Продовжуючи, ви підтверджуєте свій вік і погоджуєтеся з віковою політикою.'
        ),
        'confirm_label': 'Мені є 21 рік',
        'cta_secondary': 'ВИЙТИ',
        'subtitle': '21+',
    },
    'home': {
        'kicker': 'ДІМ БРЕНДУ',
        'title': 'ROYAL\nSMOKE',
        'body': 'Довідник дому бренду та партнерів',
        'cta_primary': 'Бренди',
        'cta_secondary': 'Дім',
        'hero': 'home/hero.jpg',
    },
    'house': {
        'kicker': 'Про дім',
        'title': 'Дім\nRoyal Smoke',
        'body': (
            'Royal Smoke — дім, що представляє в Україні родинні бренди з багаторічною історією. '
            'Тут можна дізнатися про походження брендів і познайомитися з колекцією під час візиту.'
        ),
        'cta_primary': 'Забронювати візит',
        'cta_secondary': 'Контакти',
        'hero': 'home/house.jpg',
        'blocks': [
            ('01', 'Сервіс', 'Консультації щодо брендів, історії та зберігання.'),
            ('02', 'B2B', 'Співпраця із закладами та професійними партнерами.'),
            ('03', 'Візит', 'Знайомство з домом за попереднім записом.'),
        ],
    },
    'visit': {
        'kicker': 'Дім Royal Smoke',
        'title': 'Візит',
        'cta_primary': 'Надіслати запит',
        'success_title': 'ЗАПИТ НАДІСЛАНО',
        'success_body': 'Ми звʼяжемося з вами, щоб підтвердити дату та час візиту.',
        'body_secondary': 'НОВИЙ ЗАПИТ',
    },
}

LEGAL = {
    'privacy': (
        'Політика конфіденційності',
        (
            'Ця політика пояснює, які дані може обробляти застосунок Royal Smoke і з якою метою.\n\n'
            'Royal Smoke — інформаційний довідник дому бренду. Ми збираємо лише мінімальні технічні дані, '
            'потрібні для стабільної роботи сервісу: наприклад, локально збережені бренди на вашому пристрої, '
            'базові відомості про сесію та технічні журнали для діагностики збоїв.\n\n'
            'Ми не створюємо рекламні профілі користувачів і не передаємо персональні дані третім сторонам '
            'для маркетингу.\n\n'
            'Вміст довідника призначений виключно для повнолітніх (21+). Доступ можливий лише після '
            'підтвердження віку. Якщо ви не згодні з цими умовами — припиніть користування застосунком.\n\n'
            'Запити щодо даних, доступу чи видалення інформації на пристрої можна надіслати через розділ '
            '«Контакти». Ми відповідаємо в розумні строки та в межах вимог чинного законодавства України.'
        ),
    ),
    'terms': (
        'Умови',
        (
            'Користуючись застосунком Royal Smoke, ви підтверджуєте, що вам виповнилося 21 рік і що ви '
            'ознайомилися з цими умовами.\n\n'
            'Довідник надається з інформаційною метою: опис брендів-партнерів, історії дому, лінійок і контактів. '
            'Матеріали допомогають зорієнтуватися у світі партнерів і атмосфері простору.\n\n'
            'Будь-які рішення щодо відвідування дому чи ознайомлення з матеріалами приймаєте ви самостійно, '
            'з урахуванням вікових обмежень і правил закладу.\n\n'
            'Ми можемо оновлювати тексти, зображення та структуру розділів без попереднього окремого '
            'повідомлення. Продовження користування після оновлення означає згоду з чинною редакцією умов.\n\n'
            'За порушення правил користування або надання неправдивих відомостей про вік доступ до '
            'довідника може бути обмежено. Питання щодо умов — через «Контакти».'
        ),
    ),
    'age': (
        'Вікова політика',
        (
            'Вміст довідника Royal Smoke призначений виключно для осіб, яким виповнилося 21 рік.\n\n'
            'Перед входом до основних розділів застосунок запитує підтвердження віку. Це обовʼязкова умова '
            'доступу до матеріалів про бренди, дім і повʼязаний контент. Якщо вам ще немає 21 року — '
            'будь ласка, залиште застосунок.\n\n'
            'Усі сторінки мають довідковий характер і слугують для ознайомлення з партнерами дому та '
            'його простором.\n\n'
            'Ми залишаємо за собою право оновлювати формулювання вікової політики, якщо цього вимагають '
            'зміни в законодавстві чи внутрішні стандарти дому. Актуальна версія завжди доступна в розділі «Ще».\n\n'
            'Використовуючи застосунок, ви підтверджуєте свій вік і згоду з цією політикою. Запитання — '
            'через «Контакти».'
        ),
    ),
    'about': (
        'Про застосунок',
        (
            'Royal Smoke — дім бренду і цифровий довідник його світу.\n\n'
            'Тут зібрано партнерів дому, короткі історії мануфактур, характер лінійок і контакти простору '
            'в Києві. Мета застосунку — допомогти спокійно зорієнтуватися: хто поруч із домом, чим вирізняється '
            'кожен бренд і як до нас звернутися.\n\n'
            'Довідник створено для дорослої аудиторії 21+ і розповідає про культуру, походження та атмосферу '
            'простору, який ми підтримуємо.\n\n'
            'Якщо шукаєте адресу, години роботи чи маршрут — відкрийте «Контакти». Якщо цікавлять партнери — '
            'розділ «Бренди». А щоб зрозуміти сам простір дому — зазирніть у «Дім».\n\n'
            'Дякуємо, що обираєте Royal Smoke як місце для знайомства з брендами, які ми підтримуємо.'
        ),
    ),
}


def _attach_image(instance, field_name: str, relative: str) -> bool:
    path = MOBILE_ROOT / relative
    if not path.is_file():
        return False
    field = getattr(instance, field_name)
    if field and field.name:
        return False
    with path.open('rb') as fh:
        field.save(path.name, File(fh), save=True)
    return True


class Command(BaseCommand):
    help = 'Ідемпотентний seed контенту мобільного застосунку'

    def handle(self, *args, **options):
        settings_obj = MobileSettings.load()
        updated = False
        defaults = {
            'app_version': 'Royal Smoke · v1.0',
            'app_blurb': (
                'Royal Smoke — інформаційний довідник брендів дому. Застосунок призначений для осіб 21+.'
            ),
            'contact_address': 'вул. Хрещатик, 1, Київ',
            'contact_phone': '+380 00 000 00 00',
            'contact_hours': 'Пн–Нд · 11:00–22:00',
            'contact_lat': 50.4501,
            'contact_lng': 30.5226,
        }
        for key, value in defaults.items():
            if not getattr(settings_obj, key):
                setattr(settings_obj, key, value)
                updated = True
        if updated:
            settings_obj.save()
        self.stdout.write('settings ok')

        for i, data in enumerate(BRANDS):
            brand, created = MobileBrand.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'name': data['name'],
                    'short_name': data['short_name'],
                    'mono': data['mono'],
                    'country': data['country'],
                    'panel': data['panel'],
                    'heritage': data['heritage'],
                    'sort_order': i,
                },
            )
            _attach_image(brand, 'cover', data['cover'])
            if created or not brand.facts.exists():
                brand.facts.all().delete()
                for fi, (label, value) in enumerate(data['facts']):
                    MobileBrandFact.objects.create(
                        brand=brand, label=label, value=value, sort_order=fi,
                    )
            if created or not brand.lines.exists():
                brand.lines.all().delete()
                for li, name in enumerate(data['lines']):
                    MobileBrandLine.objects.create(brand=brand, name=name, sort_order=li)
            self.stdout.write(f'brand {brand.slug} {"created" if created else "exists"}')

        for key, data in SCREENS.items():
            screen, created = MobileScreen.objects.get_or_create(
                key=key,
                defaults={
                    'kicker': data.get('kicker', ''),
                    'title': data.get('title', ''),
                    'subtitle': data.get('subtitle', ''),
                    'body': data.get('body', ''),
                    'body_secondary': data.get('body_secondary', ''),
                    'cta_primary': data.get('cta_primary', ''),
                    'cta_secondary': data.get('cta_secondary', ''),
                    'confirm_label': data.get('confirm_label', ''),
                    'legal_note': data.get('legal_note', ''),
                    'success_title': data.get('success_title', ''),
                    'success_body': data.get('success_body', ''),
                },
            )
            hero = data.get('hero')
            if hero:
                _attach_image(screen, 'hero_image', hero)
            if key == 'house' and (created or not screen.house_blocks.exists()):
                screen.house_blocks.all().delete()
                for bi, (index, title, body) in enumerate(data.get('blocks', [])):
                    MobileHouseBlock.objects.create(
                        screen=screen,
                        index_label=index,
                        title=title,
                        body=body,
                        sort_order=bi,
                    )
            self.stdout.write(f'screen {key} {"created" if created else "exists"}')

        for slug, (title, body) in LEGAL.items():
            page, created = MobileLegalPage.objects.get_or_create(
                slug=slug,
                defaults={'title': title, 'body': body},
            )
            self.stdout.write(f'page {slug} {"created" if created else "exists"}')

        self.stdout.write(self.style.SUCCESS('seed_mobile_app done'))
