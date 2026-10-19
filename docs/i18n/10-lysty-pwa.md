# Листи і PWA

Заповни лише чотири останні колонки. Не змінюй ID, місце, адресу, роль, український і англійський текст.
Один рядок — одна смислова фраза: заголовок, підзаголовок, пункт списку або цілий абзац.
HTML-теги, `href` і плейсхолдери (`{name}`, `{{ name }}`, `%s`) залиш на тих самих місцях.

| ID | Де | Адреса | Роль | Українською | Англійською | Малайська (ms) | Філіппінська (fil) | Індонезійська (id) | В'єтнамська (vi) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0991 | Листи / order_created_customer.html | templates/emails/order_created_customer.html:5 | h1 | Замовлення {{ num }} прийнято | Order {{ num }} received | Pesanan {{ num }} diterima | Natanggap ang order {{ num }} | Pesanan {{ num }} diterima | Đã nhận đơn hàng {{ num }} |
| 0992 | Листи / order_created_customer.html · Листи / order_paid.html | templates/emails/order_created_customer.html:6 · templates/emails/order_paid.html:7 | абзац | Сума | Amount | Jumlah | Halaga | Jumlah | Số tiền |
| 0993 | Листи / order_created_customer.html | templates/emails/order_created_customer.html:8 | абзац | Оплата | Payment | Pembayaran | Pagbabayad | Pembayaran | Thanh toán |
| 0994 | Листи / order_created_customer.html | templates/emails/order_created_customer.html:9 | абзац | Дякуємо, що обрали Royal Smoke. | Thank you for choosing Royal Smoke. | Terima kasih kerana memilih Royal Smoke. | Salamat sa pagpili sa Royal Smoke. | Terima kasih telah memilih Royal Smoke. | Cảm ơn bạn đã chọn Royal Smoke. |
| 0995 | Листи / order_paid.html | templates/emails/order_paid.html:5 | h1 | Оплату підтверджено | Payment confirmed | Pembayaran disahkan | Nakumpirma na ang bayad | Pembayaran dikonfirmasi | Đã xác nhận thanh toán |
| 0996 | Листи / order_paid.html | templates/emails/order_paid.html:6 | абзац | Замовлення {{ num }} | Order {{ num }} | Pesanan {{ num }} | Order {{ num }} | Pesanan {{ num }} | Đơn hàng {{ num }} |
| 0997 | Листи / order_created_customer.txt | templates/emails/order_created_customer.txt:2 | текст | Замовлення {{ num }} прийнято | Order {{ num }} received | Pesanan {{ num }} diterima | Natanggap ang order {{ num }} | Pesanan {{ num }} diterima | Đã nhận đơn hàng {{ num }} |
| 0998 | Листи / order_created_customer.txt · Листи / order_paid.txt | templates/emails/order_created_customer.txt:4 · templates/emails/order_paid.txt:4 | текст | Сума | Amount | Jumlah | Halaga | Jumlah | Số tiền |
| 0999 | Листи / order_created_customer.txt | templates/emails/order_created_customer.txt:5 | текст | Доставка | Delivery | Penghantaran | Paghahatid | Pengiriman | Giao hàng |
| 1000 | Листи / order_created_customer.txt | templates/emails/order_created_customer.txt:6 | текст | Оплата | Payment | Pembayaran | Pagbabayad | Pembayaran | Thanh toán |
| 1001 | Листи / order_created_customer.txt | templates/emails/order_created_customer.txt:8 | текст | Дякуємо, що обрали Royal Smoke. | Thank you for choosing Royal Smoke. | Terima kasih kerana memilih Royal Smoke. | Salamat sa pagpili sa Royal Smoke. | Terima kasih telah memilih Royal Smoke. | Cảm ơn bạn đã chọn Royal Smoke. |
| 1002 | Листи / booking_created_customer.txt | templates/emails/booking_created_customer.txt:2 | текст | Ваше бронювання прийнято. | Your booking has been received. | Tempahan anda telah diterima. | Natanggap na ang iyong reserbasyon. | Reservasi Anda telah diterima. | Đã nhận đặt lịch của bạn. |
| 1003 | Листи / booking_created_customer.txt | templates/emails/booking_created_customer.txt:4 | текст | Слот: {{ slot }} | Slot: {{ slot }} | Slot: {{ slot }} | Slot: {{ slot }} | Slot: {{ slot }} | Khung giờ: {{ slot }} |
| 1004 | Листи / booking_created_customer.txt | templates/emails/booking_created_customer.txt:5 | текст | Імʼя | First name | Nama | Pangalan | Nama | Tên |
| 1005 | Листи / booking_created_customer.txt | templates/emails/booking_created_customer.txt:6 | текст | Телефон | Phone | Telefon | Telepono | Telepon | Số điện thoại |
| 1006 | Листи / booking_created_customer.txt | templates/emails/booking_created_customer.txt:8 | текст | Ми звʼяжемося для підтвердження. Royal Smoke. | We will contact you to confirm. Royal Smoke. | Kami akan menghubungi anda untuk pengesahan. Royal Smoke. | Makikipag-ugnayan kami sa iyo para sa kumpirmasyon. Royal Smoke. | Kami akan menghubungi Anda untuk konfirmasi. Royal Smoke. | Chúng tôi sẽ liên hệ với bạn để xác nhận. Royal Smoke. |
| 1007 | Листи / order_paid.txt | templates/emails/order_paid.txt:2 | текст | Оплату замовлення {{ num }} підтверджено | Payment for order {{ num }} confirmed | Pembayaran untuk pesanan {{ num }} telah disahkan | Nakumpirma ang bayad para sa order {{ num }} | Pembayaran untuk pesanan {{ num }} dikonfirmasi | Đã xác nhận thanh toán cho đơn hàng {{ num }} |
| 1008 | Листи / order_paid.txt | templates/emails/order_paid.txt:5 | текст | Статус | Status | Status | Status | Status | Trạng thái |
| 1009 | PWA / офлайн-каталог | templates/pwa/offline.html:8 | текст | Каталог офлайн | Offline catalog | Katalog luar talian | Offline na katalogo | Katalog offline | Danh mục sản phẩm ngoại tuyến |
| 1010 | PWA / офлайн / stale · PWA / офлайн-каталог | templates/pwa/offline.html:14 · templates/pwa/offline.html:rs-offline-i18n | текст | Офлайн-копія каталогу. Ціни та наявність можуть бути застарілими. | Offline catalog copy. Prices and stock may be outdated. | Salinan katalog luar talian. Harga dan stok mungkin sudah lapuk. | Offline na kopya ng katalogo. Maaaring luma na ang mga presyo at stock. | Salinan katalog offline. Harga dan ketersediaan stok mungkin sudah usang. | Bản sao danh mục ngoại tuyến. Giá và tình trạng còn hàng có thể đã cũ. |
| 1011 | PWA / офлайн / catalog | templates/pwa/offline.html:rs-offline-i18n | текст | Каталог | Catalog | Katalog | Katalogo | Katalog | Sản phẩm |
| 1012 | PWA / офлайн / brands | templates/pwa/offline.html:rs-offline-i18n | текст | Бренди | Brands | Jenama | Mga brand | Merek | Thương hiệu |
| 1013 | PWA / офлайн / categories | templates/pwa/offline.html:rs-offline-i18n | текст | Категорії | Categories | Kategori | Mga kategorya | Kategori | Danh mục |
| 1014 | PWA / офлайн / all | templates/pwa/offline.html:rs-offline-i18n | текст | Усі товари | All products | Semua produk | Lahat ng produkto | Semua produk | Tất cả sản phẩm |
| 1015 | PWA / офлайн / empty | templates/pwa/offline.html:rs-offline-i18n | текст | Немає збережених даних каталогу. Підключіться до мережі, щоб оновити. | No cached catalog data. Go online to refresh. | Tiada data katalog yang disimpan. Sambung ke rangkaian untuk mengemas kini. | Walang naka-save na data ng katalogo. Kumonekta sa network para mag-refresh. | Tidak ada data katalog tersimpan. Hubungkan ke jaringan untuk memperbarui. | Không có dữ liệu danh mục đã lưu. Hãy kết nối mạng để cập nhật. |
| 1016 | PWA / офлайн / back | templates/pwa/offline.html:rs-offline-i18n | текст | Назад до каталогу | Back to catalog | Kembali ke katalog | Bumalik sa katalogo | Kembali ke katalog | Quay lại danh mục sản phẩm |
| 1017 | PWA / офлайн / stock | templates/pwa/offline.html:rs-offline-i18n | текст | На складі | In stock | Ada stok | Nasa stock | Tersedia | Còn hàng |
| 1018 | PWA / офлайн / out | templates/pwa/offline.html:rs-offline-i18n | текст | Немає в наявності | Out of stock | Kehabisan stok | Ubos na ang stock | Stok habis | Hết hàng |
| 1019 | PWA / офлайн / strength | templates/pwa/offline.html:rs-offline-i18n | текст | Міцність | Strength | Kekuatan | Lakas | Kekuatan | Độ mạnh |
| 1020 | PWA / офлайн / country | templates/pwa/offline.html:rs-offline-i18n | текст | Країна | Country | Negara | Bansa | Negara | Quốc gia |
| 1021 | PWA / офлайн / smoke | templates/pwa/offline.html:rs-offline-i18n | текст | Час куріння | Smoking time | Tempoh menghisap | Tagal ng paghithit | Durasi merokok | Thời gian hút |
| 1022 | PWA / офлайн / notes | templates/pwa/offline.html:rs-offline-i18n | текст | Смакові нотки | Flavor notes | Nota rasa | Mga nota ng lasa | Nuansa rasa | Hương vị |
| 1023 | PWA / офлайн / blend | templates/pwa/offline.html:rs-offline-i18n | текст | Бленд | Blend | Blend | Blend | Blend | Blend |
| 1024 | PWA / офлайн / updated | templates/pwa/offline.html:rs-offline-i18n | текст | Знімок | Snapshot | Syot kilat | Snapshot | Cuplikan | Ảnh chụp nhanh |
| 1025 | PWA / сповіщення | static/js/pwa.js:pushCopy | абзац | Увімкнути сповіщення про оплату та статус замовлення? | Enable notifications for payment and order status? | Hidupkan pemberitahuan untuk pembayaran dan status pesanan? | I-on ang mga notification para sa bayad at status ng order? | Aktifkan notifikasi pembayaran dan status pesanan? | Bật thông báo về thanh toán và trạng thái đơn hàng? |
| 1026 | PWA / сповіщення | static/js/pwa.js:pushCopy | кнопка | Увімкнути | Enable | Hidupkan | I-on | Aktifkan | Bật |
| 1027 | PWA / сповіщення | static/js/pwa.js:pushCopy | кнопка | Не зараз | Not now | Bukan sekarang | Hindi ngayon | Tidak sekarang | Để sau |
| 1028 | PWA / push.py | apps/pwa/services/push.py:106 | текст | Оплату підтверджено | Payment confirmed | Pembayaran disahkan | Nakumpirma na ang bayad | Pembayaran dikonfirmasi | Đã xác nhận thanh toán |
| 1029 | PWA / push.py | apps/pwa/services/push.py:107 | текст | Замовлення %(num)s оплачено. | Order %(num)s has been paid. | Pesanan %(num)s telah dibayar. | Bayad na ang order %(num)s. | Pesanan %(num)s telah dibayar. | Đơn hàng %(num)s đã được thanh toán. |
| 1030 | PWA / push.py | apps/pwa/services/push.py:111 | текст | Статус замовлення | Order status | Status pesanan | Status ng order | Status pesanan | Trạng thái đơn hàng |
| 1031 | PWA / push.py | apps/pwa/services/push.py:112 | текст | Замовлення %(num)s: %(status)s | Order %(num)s: %(status)s | Pesanan %(num)s: %(status)s | Order %(num)s: %(status)s | Pesanan %(num)s: %(status)s | Đơn hàng %(num)s: %(status)s |
| 1032 | Сторінки / повідомлення | apps/pages/views.py:134 | текст | Історія | History | Sejarah | Kasaysayan | Sejarah | Lịch sử |
