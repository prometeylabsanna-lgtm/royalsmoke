"""UK → (EN, ZH) maps for pages: delivery, contact, FAQ, legal, booking CTAs."""

from __future__ import annotations

PAGES_EXACT: dict[str, tuple[str, str]] = {
    'Обрати час': ('Choose time', '选择时间'),
    'Дегустація, консультація або візит у шоурум.': (
        'Tasting, consultation, or a showroom visit.',
        '品鉴、咨询或展厅参观。',
    ),
    'Прайс для барів, готелів і корпоративних подарунків.': (
        'Pricing for bars, hotels, and corporate gifts.',
        '酒吧、酒店及企业礼赠报价。',
    ),
    'Запросити прайс': ('Request a price list', '索取报价'),
    'Контакти': ('Contacts', '联系我们'),
    'Напишіть нам': ('Write to us', '给我们留言'),
    'Відповідаємо протягом робочого дня.': (
        'We reply during business hours.',
        '工作日内回复。',
    ),
    'Карта — Хрещатик 1': ('Map — Khreshchatyk 1', '地图——赫雷夏提克大街1号'),
    'Надіслати': ('Send', '发送'),
    'Замовити дзвінок': ('Request a call', '预约回电'),
    'Доставка і оплата': ('Delivery and payment', '配送与支付'),
    'Київ — того ж дня · Україна — 1–2 дні · ЄС — 3–5 днів.': (
        'Kyiv — same day · Ukraine — 1–2 days · EU — 3–5 days.',
        '基辅——当日 · 乌克兰——1–2天 · 欧盟——3–5天。',
    ),
    'Київ': ('Kyiv', '基辅'),
    'Україна': ('Ukraine', '乌克兰'),
    'ЄС': ('EU', '欧盟'),
    'Курʼєрська доставка того ж дня при замовленні до 15:00. Самовивіз зі шоуруму.': (
        'Same-day courier delivery when ordered before 15:00. Showroom pickup available.',
        '15:00前下单可当日快递送达。支持展厅自提。',
    ),
    "Кур'єрська доставка того ж дня при замовленні до 15:00. Самовивіз зі шоуруму.": (
        'Same-day courier delivery when ordered before 15:00. Showroom pickup available.',
        '15:00前下单可当日快递送达。支持展厅自提。',
    ),
    'Нова Пошта — 1–2 дні. Сигари пакуємо в термобокси зі страхуванням.': (
        'Nova Poshta — 1–2 days. Cigars ship in insulated boxes with insurance.',
        'Nova Poshta——1–2天。雪茄采用保温箱包装并投保。',
    ),
    'Міжнародна доставка — 3–5 робочих днів. Умови уточнюйте у менеджера.': (
        'International delivery — 3–5 business days. Ask a manager for terms.',
        '国际配送——3–5个工作日。详情请咨询经理。',
    ),
    'Способи доставки': ('Delivery methods', '配送方式'),
    'Нова Пошта, курʼєр або самовивіз — обираєте під час оформлення.': (
        'Nova Poshta, courier, or pickup — choose at checkout.',
        'Nova Poshta、快递或自提——结账时选择。',
    ),
    "Нова Пошта, кур'єр або самовивіз — обираєте під час оформлення.": (
        'Nova Poshta, courier, or pickup — choose at checkout.',
        'Nova Poshta、快递或自提——结账时选择。',
    ),
    'Оплата': ('Payment', '支付'),
    'Доступні способи оплати під час оформлення замовлення:': (
        'Payment methods available at checkout:',
        '下单时可选用的支付方式：',
    ),
    'Онлайн оплата': ('Online payment', '在线支付'),
    'банківською карткою через платіжний сервіс.': (
        'by bank card via the payment provider.',
        '通过支付服务使用银行卡。',
    ),
    'Оплата при отриманні': ('Cash on delivery', '货到付款'),
    'готівкою або карткою курʼєру / у відділенні.': (
        'cash or card to the courier / at the branch.',
        '现金或刷卡交给快递员 / 在网点支付。',
    ),
    "готівкою або карткою кур'єру / у відділенні.": (
        'cash or card to the courier / at the branch.',
        '现金或刷卡交给快递员 / 在网点支付。',
    ),
    'Безготівковий розрахунок': ('Bank transfer', '对公转账'),
    'для юридичних осіб та B2B-замовлень за рахунком.': (
        'for legal entities and B2B orders by invoice.',
        '面向企业与 B2B 订单的发票结算。',
    ),
    'Короткі відповіді про замовлення, зберігання та доставку.': (
        'Short answers about orders, storage, and delivery.',
        '关于下单、储存与配送的简要解答。',
    ),
    'Каталог': ('Catalog', '目录'),
    'Увесь каталог': ('Full catalog', '全部目录'),
    'Калькулятор': ('Calculator', '计算器'),
    'Як зберігати сигари?': ('How should I store cigars?', '如何储存雪茄？'),
    'У хумідорі при 68–72% вологості та 16–20°C. Ми відправляємо в термобоксі.': (
        'In a humidor at 68–72% humidity and 16–20°C. We ship in an insulated box.',
        '保湿盒内湿度68–72%、温度16–20°C。我们使用保温箱发货。',
    ),
    'Чи потрібна реєстрація для покупки?': (
        'Do I need an account to buy?',
        '购买是否需要注册？',
    ),
    'Ні, гостьове оформлення доступне. Кабінет зручний для повторних замовлень.': (
        'No, guest checkout is available. An account is handy for repeat orders.',
        '不必。支持游客结账。账户便于再次下单。',
    ),
    'Які терміни доставки?': ('What are the delivery times?', '配送时效如何？'),
    'Київ — часто того ж дня, Україна — 1–2 дні. Деталі на сторінці «Доставка і оплата».': (
        'Kyiv — often same day, Ukraine — 1–2 days. Details on Delivery and payment.',
        '基辅——常为当日，乌克兰——1–2天。详见「配送与支付」页。',
    ),
    'Чи можна повернути товар?': ('Can I return a product?', '可以退货吗？'),
    'Тютюнові вироби належної якості не підлягають поверненню. Брак розглядаємо індивідуально.': (
        'Tobacco products of proper quality are non-returnable. Defects are reviewed case by case.',
        '质量合格的烟草制品不可退货。瑕疵个案处理。',
    ),
    'Як працює бронювання?': ('How does booking work?', '预约如何进行？'),
    'Залиште імʼя та телефон у блоці «Бронювання» на головній — менеджер узгодить зручний час візиту.': (
        'Leave your name and phone in the Booking block on the home page — a manager will arrange a visit time.',
        '在首页「预约」区块留下姓名和电话——经理将安排方便的到访时间。',
    ),
    "Залиште ім'я та телефон у блоці «Бронювання» на головній — менеджер узгодить зручний час візиту.": (
        'Leave your name and phone in the Booking block on the home page — a manager will arrange a visit time.',
        '在首页「预约」区块留下姓名和电话——经理将安排方便的到访时间。',
    ),
    'Політика конфіденційності': ('Privacy policy', '隐私政策'),
    'Умови користування': ('Terms of use', '使用条款'),
    'Вікова політика': ('Age policy', '年龄政策'),
    'Файли cookie': ('Cookies', 'Cookie 文件'),
    '<p>Ми обробляємо персональні дані (імʼя, телефон, email, адресу доставки) лише для виконання замовлень і зворотного звʼязку. Дані не продаємо третім сторонам.</p>': (
        '<p>We process personal data (name, phone, email, delivery address) only to fulfill orders and respond to you. We do not sell data to third parties.</p>',
        '<p>我们仅出于履行订单与回复联系之目的处理个人数据（姓名、电话、邮箱、收件地址）。不会向第三方出售数据。</p>',
    ),
    "<p>Ми обробляємо персональні дані (ім'я, телефон, email, адресу доставки) лише для виконання замовлень і зворотного зв'язку. Дані не продаємо третім сторонам.</p>": (
        '<p>We process personal data (name, phone, email, delivery address) only to fulfill orders and respond to you. We do not sell data to third parties.</p>',
        '<p>我们仅出于履行订单与回复联系之目的处理个人数据（姓名、电话、邮箱、收件地址）。不会向第三方出售数据。</p>',
    ),
    '<p>Сайт Royal Smoke пропонує тютюнові вироби та аксесуари повнолітнім відвідувачам. Оформлюючи замовлення, ви підтверджуєте вік 21+ та згоду з умовами продажу.</p>': (
        '<p>Royal Smoke offers tobacco products and accessories to adult visitors. By placing an order you confirm you are 21+ and accept the sales terms.</p>',
        '<p>Royal Smoke 向成年访客提供烟草制品与配件。下单即表示您已年满21岁并同意销售条款。</p>',
    ),
    '<p>Доступ до вітрини можливий лише після підтвердження віку (cookie age_ok). Особам молодше 21 року продаж заборонено.</p>': (
        '<p>Storefront access requires age confirmation (cookie age_ok). Sales to persons under 21 are prohibited.</p>',
        '<p>进入店面前须确认年龄（cookie age_ok）。禁止向未满21岁者销售。</p>',
    ),
    '<p>Використовуємо необхідні cookies для сесії кошика, age gate та мови. Аналітичні cookies — лише за згодою, якщо увімкнено на проєкті.</p>': (
        '<p>We use necessary cookies for the cart session, age gate, and language. Analytics cookies only with consent, if enabled on the project.</p>',
        '<p>我们使用必要 Cookie 用于购物车会话、年龄门槛与语言。分析类 Cookie 仅在征得同意且项目启用时使用。</p>',
    ),
    'Нікарагуанський характер: насичений дим, чітка структура та вітоли для вечірнього ритуалу.': (
        'Nicaraguan character: rich smoke, clear structure, and vitolas for an evening ritual.',
        '尼加拉瓜风格：浓郁烟气、清晰结构，适合晚间仪式的规格。',
    ),
    'Сімейна мануфактура з глибокими blend і стабільним горінням — від Serie V до класичних ліній.': (
        'A family manufactory with deep blends and steady burn — from Serie V to classic lines.',
        '家族工坊，配方深厚、燃烧稳定——从 Serie V 到经典系列。',
    ),
    'Витримка та точність скрутки: епікюри й торо з теплими нотами дерева та кави.': (
        'Aging and precise rolling: epicures and toros with warm wood and coffee notes.',
        '陈化与精准卷制：带温暖木香与咖啡调的 Epicure 与 Toro。',
    ),
    'Мексиканське походження й насичений wrapper — сигари з характером і довгим післясмаком.': (
        'Mexican origins and a rich wrapper — cigars with character and a long finish.',
        '墨西哥血统与浓郁茄衣——个性鲜明、余韵悠长的雪茄。',
    ),
    'Приватність': ('Privacy', '隐私'),
    'Головна': ('Home', '首页'),
    'Про нас': ('About us', '关于我们'),
    'Бренди': ('Brands', '品牌'),
    'Покупка': ('Shop', '购物'),
    'Інфо': ('Info', '信息'),
    'Кошик': ('Cart', '购物车'),
    'Кабінет': ('Account', '账户'),
    'Оформлення': ('Checkout', '结算'),
    'Ваше замовлення': ('Your order', '您的订单'),
    'Підтвердити замовлення': ('Confirm order', '确认订单'),
    'Заповніть контакти та спосіб доставки.': (
        'Fill in your contacts and delivery method.',
        '请填写联系方式与配送方式。',
    ),
    'Підтверджую, що мені є 21 рік': ('I confirm I am 21 or older', '我确认已年满21岁'),
    'Каталог наповнюється.': ('The catalog is being filled.', '目录正在充实中。'),
    'Видалити': ('Remove', '删除'),
    'Кошик порожній.': ('Your cart is empty.', '购物车为空。'),
    'Продовжити покупки': ('Continue shopping', '继续购物'),
    'Оформити замовлення': ('Checkout', '去结算'),
    'Замовлення': ('Orders', '订单'),
    'Профіль': ('Profile', '个人资料'),
    'Швидкі дії': ('Quick actions', '快捷操作'),
    'Замовлень ще немає': ('No orders yet', '暂无订单'),
    'Вітаємо, {name}': ('Welcome, {name}', '欢迎，{name}'),
    'Забронювати': ('Book now', '立即预约'),
    'Оберіть послугу, дату та вільний слот.': (
        'Choose a service, date, and an open slot.',
        '请选择服务、日期与空闲时段。',
    ),
    'Вам виповнилося 21 рік?': ('Are you 21 or older?', '您是否已年满21岁？'),
    'Сайт містить інформацію про тютюнові вироби. Підтвердіть вік, щоб продовжити.': (
        'This site contains information about tobacco products. Confirm your age to continue.',
        '本站含烟草制品信息。请确认年龄后继续。',
    ),
    'Мені є 21 рік': ('I am 21+', '我已年满21岁'),
    'Мені немає 21 року': ('I am under 21', '我未满21岁'),
    'Доступ обмежено': ('Access restricted', '访问受限'),
    'Цей сайт призначений лише для повнолітніх відвідувачів 21+.': (
        'This site is only for adult visitors 21+.',
        '本站仅面向年满21岁的访客。',
    ),
    'Повернутися': ('Go back', '返回'),
    'Перший кабінет': ('First cabinet', '第一间品鉴室'),
    'Прямі мануфактури': ('Direct manufactories', '直连工坊'),
    'Власний хумідор': ('Own humidor', '自有保湿房'),
    'Бутік, каталог, сервіс': ('Boutique, catalog, service', '精品店、目录与服务'),
    'Хроніка одного рішення': ('Chronicle of one decision', '一个决定的编年'),
    'років на ринку': ('years on the market', '年市场经验'),
    'Почали з невеликого простору в Києві: кілька полиць, ручний відбір і розмова з кожним гостем замість випадкової вітрини.': (
        'We started in a small Kyiv space: a few shelves, hand selection, and a talk with every guest instead of a random showcase.',
        '我们从基辅的一小间空间起步：几排货架、手工甄选，以及与每位客人的交谈，而非随意陈列。',
    ),
    'Налагодили прямі поставки з Нікарагуа, Домінікани та Куби — без зайвих посередників, з чесною ціною і стабільною якістю партій.': (
        'We set up direct supply from Nicaragua, the Dominican Republic, and Cuba — without extra middlemen, with fair pricing and stable batch quality.',
        '我们打通来自尼加拉瓜、多米尼加与古巴的直供——减少中间环节，价格公道，批次质量稳定。',
    ),
    'Збудували сховище зі стабільною вологістю й зібрали команду сомельє, яка супроводжує замовлення від першої консультації до доставки.': (
        'We built a storage room with stable humidity and a sommelier team that guides each order from the first consult to delivery.',
        '我们打造湿度稳定的仓储，并组建侍茄师团队，从首次咨询到配送全程陪伴订单。',
    ),
    'Працюємо як бутік і як точний онлайн-каталог: консультація, термобокс і доставка, яка береже лист.': (
        'We work as a boutique and a precise online catalog: consultation, insulated boxing, and delivery that protects the leaf.',
        '我们既是精品店也是精准在线目录：咨询、保温包装，以及呵护烟叶的配送。',
    ),
    'Royal Smoke — tobacco atelier, зібраний навколо простого правила: продавати лише те, що самі готові курити.': (
        'Royal Smoke is a tobacco atelier built around a simple rule: sell only what we are ready to smoke ourselves.',
        'Royal Smoke 是围绕一条简单规则打造的烟草工坊：只卖我们自己也愿意品吸的东西。',
    ),
}
