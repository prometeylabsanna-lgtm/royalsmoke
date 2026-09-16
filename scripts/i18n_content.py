"""Exact UK → (EN, ZH) maps for CMS / catalog modeltranslation fields."""

from __future__ import annotations

import re

from i18n_content_pages import PAGES_EXACT

CYRILLIC_RE = re.compile(r'[а-яА-ЯёЁіІїЇєЄґҐ]')

EXACT: dict[str, tuple[str, str]] = {
    **PAGES_EXACT,
    'Історія': ('History', '历史'),
    'Про Royal Smoke': ('About Royal Smoke', '关于 Royal Smoke'),
    'Ключові категорії': ('Key categories', '重点分类'),
    'Tobacco Atelier': ('Tobacco Atelier', 'Tobacco Atelier'),
    'Новинки': ('New arrivals', '新品'),
    'Сервіс': ('Service', '服务'),
    'Топ продажів': ('Best sellers', '热销榜'),
    'B2B': ('B2B', 'B2B'),
    'Бронювання': ('Booking', '预约'),
    'Калькулятор підбору': ('Selection calculator', '选茄计算器'),
    'Доставка': ('Delivery', '配送'),
    'Акції': ('Sale', '促销'),
    'Сигари': ('Cigars', '雪茄'),
    'Сигарети': ('Cigarettes', '香烟'),
    'Аксесуари': ('Accessories', '配件'),
    'До каталогу': ('To catalog', '前往目录'),
    'Читати далі': ('Read more', '阅读更多'),
    'Сьогодні': ('Today', '今天'),
    'XIX ст.': ('19th c.', '19世纪'),
    'Intro': ('Intro', 'Intro'),
    '1492+': ('1492+', '1492+'),
    'Core': ('Core', 'Core'),
    'Міцність': ('Strength', '浓度'),
    'Формат': ('Format', '规格'),
    'Країна': ('Country', '产地'),
    'Бюджет': ('Budget', '预算'),
    'Легка': ('Mild', '轻度'),
    'Середня': ('Medium', '中度'),
    'Середньо-повна': ('Medium-full', '中重度'),
    'Повна': ('Full', '重度'),
    'Куба': ('Cuba', '古巴'),
    'Нікарагуа': ('Nicaragua', '尼加拉瓜'),
    'Домінікана': ('Dominican Republic', '多米尼加'),
    'Мексика': ('Mexico', '墨西哥'),
    'Гондурас': ('Honduras', '洪都拉斯'),
    'Будь-яка': ('Any', '任意'),
    'до 1000 ₴': ('up to 1000 ₴', '1000 ₴ 以内'),
    'до 1500 ₴': ('up to 1500 ₴', '1500 ₴ 以内'),
    'до 2500 ₴': ('up to 2500 ₴', '2500 ₴ 以内'),
    '1000—2000 ₴': ('1000—2000 ₴', '1000—2000 ₴'),
    '2000—3500 ₴': ('2000—3500 ₴', '2000—3500 ₴'),
    'без обмежень': ('no limit', '不限'),
    'Дегустація': ('Tasting', '品鉴'),
    'Консультація сомельє': ('Sommelier consultation', '侍茄师咨询'),
    'Візит у шоурум': ('Showroom visit', '展厅参观'),
    'Самовивіз': ('Pickup', '自提'),
    'Київ, Україна': ('Kyiv, Ukraine', '基辅，乌克兰'),
    'Пн–Нд: 11:00–21:00': ('Mon–Sun: 11:00–21:00', '周一至周日：11:00–21:00'),
    '45–60 хв': ('45–60 min', '45–60 分钟'),
    '35–45 хв': ('35–45 min', '35–45 分钟'),
    '60–75 хв': ('60–75 min', '60–75 分钟'),
    '75–90 хв': ('75–90 min', '75–90 分钟'),
    'Гільйотина Classic': ('Guillotine Classic', '吉列刀 Classic'),
    'ракурс 2': ('angle 2', '角度 2'),
    'деталі wrapper': ('wrapper details', '茄衣细节'),
    'Олександр': ('Alexander', '亚历山大'),
    'Михайло': ('Michael', '迈克尔'),
    'Ірина': ('Irene', '伊琳娜'),
    'Дмитро': ('Dmitry', '德米特里'),
    'Катерина': ('Catherine', '叶卡捷琳娜'),
    'Андрій': ('Andrew', '安德鲁'),
    'Юлія': ('Julia', '尤莉娅'),
    'Дерево, кава, шкіра': ('Wood, coffee, leather', '木质、咖啡、皮革'),
    'Дерево, кедр, легка солодкість, білий перець.': (
        'Wood, cedar, light sweetness, white pepper.',
        '木质、雪松、淡甜、白胡椒。',
    ),
    'Ми відбираємо сигари вручну, зберігаємо їх у власних хумідорах і допомагаємо знайти вітолу під ваш ритуал.': (
        'We select cigars by hand, keep them in our own humidors, and help you find a vitola for your ritual.',
        '我们手工甄选雪茄，存放于自有保湿房，并帮您找到适合个人仪式的规格。',
    ),
    'Оберіть слот на дегустацію, консультацію або візит у шоурум.': (
        'Choose a slot for a tasting, consultation, or showroom visit.',
        '选择品鉴、咨询或展厅参观的时段。',
    ),
    'Залиште контакти — менеджер узгодить зручний час візиту.': (
        'Leave your contacts — a manager will arrange a convenient visit time.',
        '留下联系方式——经理将安排方便的参观时间。',
    ),
    'Залиште контакти — менеджер узгодить зручний час візиту. Ми передзвонимо протягом робочого дня, щоб підтвердити слот і відповісти на запитання. Можна обрати дегустацію, консультацію сомельє або спокійний візит у шоурум — підлаштуємось під ваш ритм.': (
        'Leave your contacts — a manager will arrange a convenient visit time. We will call back during business hours to confirm the slot and answer questions. Choose a tasting, sommelier consultation, or a quiet showroom visit — we adapt to your pace.',
        '留下联系方式——经理将安排方便的参观时间。我们会在工作日内回电确认时段并解答疑问。可选品鉴、侍茄师咨询或安静的展厅到访——我们按您的节奏安排。',
    ),
    'Прайс і умови для барів, готелів і корпоративних подарунків.': (
        'Pricing and terms for bars, hotels, and corporate gifts.',
        '酒吧、酒店及企业礼赠的价格与条款。',
    ),
    'Чотири кроки — три рекомендації з поясненням.': (
        'Four steps — three recommendations with explanations.',
        '四步流程——三项推荐并附说明。',
    ),
    'Київ — того ж дня, Україна — 1–2 дні. Термобокси для сигар.': (
        'Kyiv — same day, Ukraine — 1–2 days. Insulated boxes for cigars.',
        '基辅——当日达，乌克兰——1–2天。雪茄专用保温箱。',
    ),
    'Сигари, відібрані вручну для тих, хто знає різницю.': (
        'Cigars handpicked for those who know the difference.',
        '为懂行之人手工甄选雪茄。',
    ),
    'Пошук сигар, брендів, аксесуарів…': (
        'Search cigars, brands, accessories…',
        '搜索雪茄、品牌、配件…',
    ),
    'Сигари, відібрані вручну для тих, хто знає різницю': (
        'Cigars handpicked for those who know the difference',
        '为懂行之人手工甄选雪茄',
    ),
    'Понад 400 позицій з мануфактур Нікарагуа, Домінікани та Куби.': (
        'Over 400 items from manufactories in Nicaragua, the Dominican Republic, and Cuba.',
        '来自尼加拉瓜、多米尼加和古巴工厂的400余款产品。',
    ),
    'Лімітовані лінії AJ Fernandez уже в наявності': (
        'Limited AJ Fernandez lines are now in stock',
        'AJ Fernandez 限量系列现已到货',
    ),
    'Bellas Artes, New World, Enclave — повні вітоли та подарункові набори.': (
        'Bellas Artes, New World, Enclave — full vitolas and gift sets.',
        'Bellas Artes、New World、Enclave——完整规格与礼盒套装。',
    ),
    'Аксесуари, які тримають ритуал': (
        'Accessories that hold the ritual',
        '守护仪式的配件',
    ),
    'Хумідори, гільйотини, попільниці та футляри від європейських майстерень.': (
        'Humidors, guillotines, ashtrays, and cases from European workshops.',
        '来自欧洲工坊的保湿盒、吉列刀、烟灰缸与皮套。',
    ),
    'Темний тютюн. Теплий ритуал.': (
        'Dark tobacco. A warm ritual.',
        '深色烟草。温暖的仪式。',
    ),
    'Відбірні сигари для вечора без компромісів.': (
        'Selected cigars for an uncompromising evening.',
        '为毫不妥协的夜晚甄选雪茄。',
    ),
    'Пакування, гідне ритуалу': (
        'Packaging worthy of the ritual',
        '配得上仪式的包装',
    ),
    'Подарункові набори та лімітовані вітоли в фірмових коробках.': (
        'Gift sets and limited vitolas in branded boxes.',
        '品牌盒装礼盒与限量规格。',
    ),
    'Карибські витоки': ('Caribbean origins', '加勒比起源'),
    'Золота доба': ('Golden age', '黄金时代'),
    'Новий світ': ('New World', '新世界'),
    'Сигара — це повільний ритуал: від древніх обрядів до майстрів скрутки. У Royal Smoke ми бережемо цей темп — добірний лист, тиша хумідора і дим, вартуючий уваги.': (
        'A cigar is a slow ritual: from ancient rites to master rollers. At Royal Smoke we keep that pace — chosen leaf, the quiet of the humidor, and smoke worth attention.',
        '雪茄是缓慢的仪式：从古老礼俗到卷制大师。在 Royal Smoke，我们守护这份节奏——精选烟叶、保湿房的静谧，以及值得凝神的烟气。',
    ),
    'У Карибах дим був мовою зустрічі й обряду, а не розвагою. Саме тут народжується шлях сигари — від живого листа до ритуалу часу.': (
        'In the Caribbean, smoke was a language of meeting and rite, not entertainment. This is where the cigar’s path begins — from living leaf to a ritual of time.',
        '在加勒比，烟气是相会与仪礼的语言，而非娱乐。雪茄之路正从此处开始——从鲜叶到时间的仪式。',
    ),
    'Куба XIX століття задає канон: вітола, дисципліна скрутки, імена легенд. Сигара стає мовою смаку й статусу — витонченою й безкомпромісною.': (
        'Nineteenth-century Cuba sets the canon: vitola, rolling discipline, legendary names. The cigar becomes a language of taste and status — refined and uncompromising.',
        '十九世纪的古巴奠定典范：规格、卷制纪律、传奇之名。雪茄成为品味与身份的语言——精致且毫不妥协。',
    ),
    'Смак уже не має однієї адреси: Нікарагуа, Домінікана, Гондурас. Ми обираємо мануфактури за характером диму — тихо, точно, без зайвого шуму.': (
        'Flavor no longer has a single address: Nicaragua, the Dominican Republic, Honduras. We choose manufactories by the character of the smoke — quietly, precisely, without extra noise.',
        '风味已不再只有一个地址：尼加拉瓜、多米尼加、洪都拉斯。我们按烟气性格选择工厂——安静、准确、不事张扬。',
    ),
    'Рекомендуємо 30–40 хвилин відпочинку в хумідорі перед розкурюванням.': (
        'We recommend 30–40 minutes of rest in a humidor before lighting.',
        '建议点燃前在保湿盒中静置30–40分钟。',
    ),
    'Ідеальна для вечірнього ритуалу з single malt або espresso.': (
        'Ideal for an evening ritual with a single malt or espresso.',
        '适合搭配单一麦芽威士忌或意式浓缩的晚间仪式。',
    ),
    'Для досвідчених палінь: повільний темп, щоб розкрити складний blend.': (
        'For experienced smokers: a slow pace to open up a complex blend.',
        '适合资深品吸者：放慢节奏以展开复杂配方。',
    ),
    'Краще з темним шоколадом 70%+ або кавою cold brew.': (
        'Best with 70%+ dark chocolate or cold-brew coffee.',
        '宜搭配70%以上黑巧克力或冷萃咖啡。',
    ),
    'Підійде після легкої вечері — не перевантажує смаковий баланс.': (
        'Suits a light dinner — it will not overload the palate.',
        '适合轻食晚餐后——不会压过味觉平衡。',
    ),
    'Для вечора після роботи — саме те. Нотки кави відчуваються чітко.': (
        'Just right for an evening after work. Coffee notes come through clearly.',
        '下班后的夜晚刚刚好。咖啡香清晰可辨。',
    ),
    'Подарункова упаковка не потрібна — сам продукт говорить за себе.': (
        'Gift wrapping is unnecessary — the product speaks for itself.',
        '不必礼盒包装——产品本身已足够说明。',
    ),
    'Порівнював з іншими vitolas цієї лінії — ця мʼякша, але з характером.': (
        'Compared with other vitolas in this line — this one is milder, yet has character.',
        '与同系列其他规格相比——这支更柔和，但仍有性格。',
    ),
    'Рівне горіння, без гіркоти. Взяли ще раз у коробку.': (
        'Even burn, no bitterness. We bought another box.',
        '燃烧均匀，无苦味。又买了一盒。',
    ),
    'Сервіс Royal Smoke як завжди — сигара приїхала в ідеальній вологості.': (
        'Royal Smoke service as always — the cigar arrived at perfect humidity.',
        'Royal Smoke 的服务一如既往——雪茄以理想湿度送达。',
    ),
}

_SELECTED_UK = '. Відібрано для Royal Smoke.'
_DETAIL_PREFIX = 'Детальний опис '
_DETAIL_SUFFIX = '. Зберігання у власних хумідорах.'


def _lookup(text: str) -> tuple[str, str] | None:
    if text in EXACT:
        return EXACT[text]
    alt = text.replace("'", 'ʼ').replace('ʼ', "'")
    if alt in EXACT:
        return EXACT[alt]
    return None


def _apply_fragments(text: str) -> tuple[str, str]:
    en, zh = text, text
    for uk, (e, z) in sorted(EXACT.items(), key=lambda kv: len(kv[0]), reverse=True):
        if uk and uk in en:
            en = en.replace(uk, e)
        if uk and uk in zh:
            zh = zh.replace(uk, z)
    return en, zh


def translate_uk(text: str | None) -> tuple[str, str] | None:
    raw = (text or '').strip()
    if not raw:
        return None
    try:
        from apps.core.legal_privacy_body import (
            PRIVACY_BODY_EN,
            PRIVACY_BODY_UK,
            PRIVACY_BODY_ZH,
        )

        if raw == PRIVACY_BODY_UK.strip():
            return PRIVACY_BODY_EN, PRIVACY_BODY_ZH
        # Legacy short privacy blurbs → full policy
        short_uk = (
            '<p>Ми обробляємо персональні дані (імʼя, телефон, email, адресу доставки) '
            'лише для виконання замовлень і зворотного звʼязку. Дані не продаємо третім сторонам.</p>'
        )
        short_uk_alt = short_uk.replace("ʼ", "'")
        if raw in {short_uk, short_uk_alt, short_uk.replace("'", "ʼ")}:
            return PRIVACY_BODY_EN, PRIVACY_BODY_ZH
    except ImportError:
        pass
    hit = _lookup(raw)
    if hit:
        return hit
    if raw.endswith(_SELECTED_UK):
        name = raw[: -len(_SELECTED_UK)]
        name_en, name_zh = translate_uk(name) or (name, name)
        return (
            f'{name_en}. Selected for Royal Smoke.',
            f'{name_zh}。为 Royal Smoke 甄选。',
        )
    if raw.startswith(_DETAIL_PREFIX) and raw.endswith(_DETAIL_SUFFIX):
        name = raw[len(_DETAIL_PREFIX) : -len(_DETAIL_SUFFIX)]
        name_en, name_zh = translate_uk(name) or (name, name)
        return (
            f'Detailed profile of {name_en}. Stored in our humidors.',
            f'{name_zh} 的详细介绍。存放于我们的保湿房。',
        )
    en, zh = _apply_fragments(raw)
    if en != raw or zh != raw:
        if CYRILLIC_RE.search(en) or CYRILLIC_RE.search(zh):
            return None
        return en, zh
    if not CYRILLIC_RE.search(raw):
        return raw, raw
    return None
