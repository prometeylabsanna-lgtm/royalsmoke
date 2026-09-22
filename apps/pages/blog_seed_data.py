"""Metadata + FAQ for blog seed posts."""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

KYIV = ZoneInfo('Europe/Kyiv')
_BASE = datetime(2026, 9, 10, 11, 0, tzinfo=KYIV)

POSTS: list[dict] = [
    {
        'slug': 'yak-obraty-pershu-sygaru',
        'sort_order': 10,
        'published_at': _BASE,
        'cover': 'static/img/blog/01-first-cigar.jpg',
        'title_uk': 'Як обрати першу сигару: гід для новачків',
        'title_en': 'How to choose your first cigar: a beginner’s guide',
        'title_zh': '如何选择第一支雪茄：新手指南',
        'excerpt_uk': (
            'Міцність, вітола й ритуал підпалу — короткий алгоритм, '
            'щоб перша сигара принесла смак, а не розчарування.'
        ),
        'excerpt_en': (
            'Strength, vitola, and the lighting ritual — a short path so your '
            'first cigar brings flavor, not frustration.'
        ),
        'excerpt_zh': '劲头、维托拉与点火仪式——让第一支雪茄带来风味而非失望的实用路径。',
        'meta_title_uk': 'Як обрати першу сигару — гід для новачків',
        'meta_title_en': 'How to choose your first cigar — beginner guide',
        'meta_title_zh': '如何选择第一支雪茄——新手指南',
        'meta_description_uk': (
            'Як обрати першу сигару: міцність, вітола, обгортка й ритуал. '
            'Поради сомельє Royal Smoke з посиланнями на каталог.'
        ),
        'meta_description_en': (
            'How to choose your first cigar: strength, vitola, wrapper, ritual. '
            'Royal Smoke sommelier tips with catalog links.'
        ),
        'meta_description_zh': '如何选择第一支雪茄：劲头、维托拉、茄衣与仪式。Royal Smoke 侍茄师建议。',
        'cover_alt_uk': 'Три сигари на дереві з каттером — гід для першої сигари, Royal Smoke',
        'cover_alt_en': 'Three cigars on wood with a cutter — first cigar guide, Royal Smoke',
        'cover_alt_zh': '木桌上的三支雪茄与切刀——第一支雪茄指南，Royal Smoke',
        'faq': [
            {
                'q_uk': 'Яку міцність обрати для першої сигари?',
                'a_uk': 'Почніть з легкої або середньої. Повна міцність на старті часто маскує смак і швидше втомлює.',
                'q_en': 'Which strength for a first cigar?',
                'a_en': 'Start mild or medium. Full strength early often hides flavor and tires you faster.',
                'q_zh': '第一支雪茄选什么劲头？',
                'a_zh': '从轻度或中度开始。一上来选全劲常会掩盖风味并更快让人疲劳。',
            },
            {
                'q_uk': 'Robusto чи Corona для старту?',
                'a_uk': 'Обидва формати дружні до новачка. Robusto дає довший ритуал; Corona — коротшу сесію.',
                'q_en': 'Robusto or Corona to start?',
                'a_en': 'Both are beginner-friendly. Robusto lasts longer; Corona fits a shorter session.',
                'q_zh': '新手选 Robusto 还是 Corona？',
                'a_zh': '两者都适合入门。Robusto 更长；Corona 适合更短的时段。',
            },
            {
                'q_uk': 'Скільки сигар купити вперше?',
                'a_uk': 'Достатньо 1–3 різних профілів середньої міцності, щоб зрозуміти смакові вподобання.',
                'q_en': 'How many cigars to buy first?',
                'a_en': 'One to three different medium profiles is enough to learn your taste.',
                'q_zh': '第一次买几支合适？',
                'a_zh': '先买 1–3 支不同风味的中度雪茄，足以了解偏好。',
            },
            {
                'q_uk': 'Чи потрібен хумідор одразу?',
                'a_uk': 'Якщо не викурюєте за кілька днів — так, або travel-бокс з регулятором вологості.',
                'q_en': 'Do I need a humidor immediately?',
                'a_en': 'If you will not smoke them within days — yes, or a travel case with humidity control.',
                'q_zh': '需要马上买保湿盒吗？',
                'a_zh': '若几天内抽不完，需要保湿盒或带湿度控制的旅行盒。',
            },
        ],
    },
    {
        'slug': 'yak-zberigaty-sygary-humidora',
        'sort_order': 20,
        'published_at': _BASE + timedelta(days=2),
        'cover': 'static/img/blog/02-humidor.jpg',
        'title_uk': 'Як зберігати сигари: вологість і хумідор',
        'title_en': 'How to store cigars: humidity and humidors',
        'title_zh': '如何保存雪茄：湿度与保湿盒',
        'excerpt_uk': (
            '65–70% RH, стабільна температура й правильний регулятор — '
            'база, без якої навіть преміальний лист втрачає характер.'
        ),
        'excerpt_en': (
            '65–70% RH, stable temperature, and the right regulator — '
            'the base without which even premium leaf loses character.'
        ),
        'excerpt_zh': '65–70% 相对湿度、稳定温度与正确调节——高端叶片也离不开的基础。',
        'meta_title_uk': 'Як зберігати сигари в хумідорі — вологість',
        'meta_title_en': 'How to store cigars in a humidor — humidity',
        'meta_title_zh': '如何用保湿盒保存雪茄——湿度指南',
        'meta_description_uk': (
            'Зберігання сигар: 65–70% вологості, типи хумідорів, регулятори '
            'та помилки, яких уникати. Гід Royal Smoke.'
        ),
        'meta_description_en': (
            'Cigar storage: 65–70% humidity, humidor types, packs, and mistakes '
            'to avoid. A Royal Smoke guide.'
        ),
        'meta_description_zh': '雪茄保存：65–70% 湿度、保湿盒类型、调节包与常见错误。Royal Smoke 指南。',
        'cover_alt_uk': 'Відкритий хумідор із сигарами та гігрометром, Royal Smoke',
        'cover_alt_en': 'Open humidor with cigars and a hygrometer, Royal Smoke',
        'cover_alt_zh': '打开的保湿盒、雪茄与湿度计，Royal Smoke',
        'faq': [
            {
                'q_uk': 'Яка вологість оптимальна для сигар?',
                'a_uk': 'Зазвичай 65–70% RH при стабільній кімнатній температурі без стрибків.',
                'q_en': 'What humidity is ideal for cigars?',
                'a_en': 'Usually 65–70% RH with stable room temperature and no sharp swings.',
                'q_zh': '雪茄理想湿度是多少？',
                'a_zh': '通常为 65–70% 相对湿度，室温稳定、避免剧烈波动。',
            },
            {
                'q_uk': 'Чи можна тримати сигари в холодильнику?',
                'a_uk': 'Ні. Конденсат і запахи їжі псують лист. Потрібен хумідор або герметичний бокс з регулятором.',
                'q_en': 'Can I keep cigars in the fridge?',
                'a_en': 'No. Condensation and food odors damage the leaf. Use a humidor or sealed case with a pack.',
                'q_zh': '雪茄可以放冰箱吗？',
                'a_zh': '不可以。冷凝与食物气味会损害叶片。请用保湿盒或带调节包的密封盒。',
            },
            {
                'q_uk': 'Що таке seasoning хумідора?',
                'a_uk': 'Це підготовка порожньої скриньки до робочої вологості перед завантаженням сигар.',
                'q_en': 'What is humidor seasoning?',
                'a_en': 'Preparing an empty box to working humidity before loading cigars.',
                'q_zh': '什么是保湿盒 seasoning？',
                'a_zh': '在放入雪茄前，先把空盒调节到工作湿度。',
            },
            {
                'q_uk': 'Як зрозуміти, що сигара пересохла?',
                'a_uk': 'Обгортка стає ламкою, горіння швидке й гаряче, смак плоский. Потрібна поступова регідратація.',
                'q_en': 'How do I know a cigar is too dry?',
                'a_en': 'The wrapper turns brittle, burn runs hot and fast, flavor flattens. Rehydrate gradually.',
                'q_zh': '如何判断雪茄过干？',
                'a_zh': '茄衣变脆、燃烧又快又烫、风味变平。需逐步回潮。',
            },
        ],
    },
    {
        'slug': 'aksessuary-dlya-sygar-katter-zapalnychka',
        'sort_order': 30,
        'published_at': _BASE + timedelta(days=4),
        'cover': 'static/img/blog/03-accessories.jpg',
        'title_uk': 'Аксесуари для сигар: каттер, запальничка, попільниця',
        'title_en': 'Cigar accessories: cutter, lighter, ashtray',
        'title_zh': '雪茄配件：切刀、打火机、烟灰缸',
        'excerpt_uk': (
            'Базовий набір інструментів, без яких навіть добра сигара '
            'грає нижче свого потенціалу.'
        ),
        'excerpt_en': (
            'The essential tool kit — without it even a good cigar plays below its potential.'
        ),
        'excerpt_zh': '基础工具组合——没有它们，再好的雪茄也发挥不出潜力。',
        'meta_title_uk': 'Аксесуари для сигар — каттер і запальничка',
        'meta_title_en': 'Cigar accessories — cutter and lighter guide',
        'meta_title_zh': '雪茄配件——切刀与打火机指南',
        'meta_description_uk': (
            'Каттер, бутанова запальничка й попільниця: як обрати аксесуари '
            'для сигар і не зіпсувати смак. Royal Smoke.'
        ),
        'meta_description_en': (
            'Cutter, butane lighter, ashtray: how to choose cigar accessories '
            'without ruining flavor. Royal Smoke.'
        ),
        'meta_description_zh': '切刀、丁烷打火机与烟灰缸：如何挑选雪茄配件且不破坏风味。Royal Smoke。',
        'cover_alt_uk': 'Каттер, запальничка і попільниця — набір аксесуарів, Royal Smoke',
        'cover_alt_en': 'Cutter, lighter and ashtray — accessory set, Royal Smoke',
        'cover_alt_zh': '切刀、打火机与烟灰缸——配件套装，Royal Smoke',
        'faq': [
            {
                'q_uk': 'Який каттер найкращий для новачка?',
                'a_uk': 'Подвійна гілотина з гострими лезами й отвором під ваш ring gauge — найуніверсальніший вибір.',
                'q_en': 'Best cutter for beginners?',
                'a_en': 'A sharp double guillotine sized for your ring gauge is the most universal choice.',
                'q_zh': '新手最适合什么切刀？',
                'a_zh': '锋利的双刃闸刀，开口匹配你的环径，是最通用的选择。',
            },
            {
                'q_uk': 'Чому не варто запалювати бензином?',
                'a_uk': 'Аромат палива змішується з димом і маскує нотки листа. Для сигар потрібен чистий бутан.',
                'q_en': 'Why avoid gasoline lighters?',
                'a_en': 'Fuel aroma mixes into the smoke and hides leaf notes. Use clean butane.',
                'q_zh': '为什么不建议用汽油打火机？',
                'a_zh': '燃油气味会混入烟气并掩盖叶片香气。请使用无味丁烷。',
            },
            {
                'q_uk': 'Soft-flame чи torch?',
                'a_uk': 'Soft-flame м’якший для підпалу вдома; torch зручний на вітрі, але легко перегріває край.',
                'q_en': 'Soft-flame or torch?',
                'a_en': 'Soft-flame is gentler indoors; torch helps outdoors but overheats if held too close.',
                'q_zh': '柔焰还是喷枪？',
                'a_zh': '室内柔焰更温和；户外喷枪更方便，但太近容易过热。',
            },
            {
                'q_uk': 'Чи потрібна дорога попільниця?',
                'a_uk': 'Важливі глибина, стійкість і жолобки. Матеріал — на смак, функція важливіша за бренд.',
                'q_en': 'Do I need an expensive ashtray?',
                'a_en': 'Depth, stability, and rests matter most. Function beats brand prestige.',
                'q_zh': '烟灰缸一定要很贵吗？',
                'a_zh': '深度、稳定与托槽更重要。功能优先于品牌溢价。',
            },
        ],
    },
    {
        'slug': 'yak-chytaty-vitolu-micnist-kilce',
        'sort_order': 40,
        'published_at': _BASE + timedelta(days=6),
        'cover': 'static/img/blog/04-vitola.jpg',
        'title_uk': 'Як читати вітолу, міцність і кільце сигари',
        'title_en': 'How to read vitola, strength, and the cigar band',
        'title_zh': '如何阅读维托拉、劲头与茄标',
        'excerpt_uk': (
            'Розмір, ring gauge і шкала міцності — як зчитувати картку товару '
            'і не плутати маркетинг кільця зі смаком.'
        ),
        'excerpt_en': (
            'Size, ring gauge, and strength — how to read a product card '
            'without confusing band marketing with flavor.'
        ),
        'excerpt_zh': '尺寸、环径与劲头——如何读懂商品卡，而不把茄标营销当成风味。',
        'meta_title_uk': 'Вітола і міцність сигари — як читати',
        'meta_title_en': 'Cigar vitola and strength — how to read them',
        'meta_title_zh': '雪茄维托拉与劲头——如何阅读',
        'meta_description_uk': (
            'Що означають вітола, ring gauge, міцність і кільце сигари. '
            'Практичний гід Royal Smoke для вибору в каталозі.'
        ),
        'meta_description_en': (
            'What vitola, ring gauge, strength, and the cigar band mean. '
            'A practical Royal Smoke catalog guide.'
        ),
        'meta_description_zh': '维托拉、环径、劲头与茄标分别意味着什么。Royal Smoke 实用选购指南。',
        'cover_alt_uk': 'Сигари різної вітоли з вимірювальним інструментом, Royal Smoke',
        'cover_alt_en': 'Cigars of different vitolas with a measuring tool, Royal Smoke',
        'cover_alt_zh': '不同维托拉雪茄与测量工具，Royal Smoke',
        'faq': [
            {
                'q_uk': 'Що таке ring gauge?',
                'a_uk': 'Це діаметр сигари в шістдесят четвертих дюйма. Вищий ring — товстіша сигара.',
                'q_en': 'What is ring gauge?',
                'a_en': 'Cigar diameter in sixty-fourths of an inch. Higher ring means a thicker cigar.',
                'q_zh': '什么是 ring gauge？',
                'a_zh': '以六十四分之一英寸表示的直径。环径越大，雪茄越粗。',
            },
            {
                'q_uk': 'Чи означає повна міцність кращу якість?',
                'a_uk': 'Ні. Міцність — про відчуття тіла й нікотину, а не про клас листа.',
                'q_en': 'Does full strength mean better quality?',
                'a_en': 'No. Strength describes body and nicotine feel, not leaf quality.',
                'q_zh': '全劲等于更高品质吗？',
                'a_zh': '不等于。劲头描述身体感受与尼古丁强度，不是叶片等级。',
            },
            {
                'q_uk': 'Коли знімати кільце?',
                'a_uk': 'Коли клей прогрівся — часто після першої третини — щоб не порвати обгортку.',
                'q_en': 'When to remove the band?',
                'a_en': 'Once adhesive softens — often after the first third — to avoid tearing the wrapper.',
                'q_zh': '何时取下茄标？',
                'a_zh': '等胶质受热软化后——常在前三分之一之后——以免撕破茄衣。',
            },
            {
                'q_uk': 'Як обрати вітолу під час вечора?',
                'a_uk': 'Оцініть вільний час: corona на коротку паузу, robusto/toro — на спокійну годину.',
                'q_en': 'How to pick a vitola for the evening?',
                'a_en': 'Match free time: corona for a short pause, robusto/toro for a calm hour.',
                'q_zh': '如何按晚上时间选维托拉？',
                'a_zh': '按空闲时间：短暂停选 corona，安静一小时选 robusto/toro。',
            },
        ],
    },
]
