# Бронювання, калькулятор, контакти, B2B

Заповни лише чотири останні колонки. Не змінюй ID, місце, адресу, роль, український і англійський текст.
Один рядок — одна смислова фраза: заголовок, підзаголовок, пункт списку або цілий абзац.
HTML-теги, `href` і плейсхолдери (`{name}`, `{{ name }}`, `%s`) залиш на тих самих місцях.

| ID | Де | Адреса | Роль | Українською | Англійською | Малайська (ms) | Філіппінська (fil) | Індонезійська (id) | В'єтнамська (vi) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0566 | Бронювання / сторінка | templates/booking/page.html:18 | підпис | Послуга | Service | Perkhidmatan | Serbisyo | Layanan | Dịch vụ |
| 0567 | Бронювання / сторінка | templates/booking/page.html:24 | варіант | Оберіть послугу | Select a service | Pilih perkhidmatan | Pumili ng serbisyo | Pilih layanan | Chọn dịch vụ |
| 0568 | Бронювання / сторінка | templates/booking/page.html:32 | підпис | Дата | Date | Tarikh | Petsa | Tanggal | Ngày |
| 0569 | Бронювання / сторінка | templates/booking/page.html:45 | підпис | Імʼя | First name | Nama | Pangalan | Nama | Tên |
| 0570 | Бронювання / сторінка | templates/booking/page.html:50 | підпис | Телефон | Phone | Telefon | Telepono | Telepon | Số điện thoại |
| 0571 | Бронювання / сторінка | templates/booking/page.html:60 | підпис | Побажання | Notes | Catatan | Mga tala | Catatan | Ghi chú |
| 0572 | Бронювання / слоти | templates/booking/partials/slots.html:2 | підпис | Час | Time | Masa | Oras | Waktu | Giờ |
| 0573 | Бронювання / слоти | templates/booking/partials/slots.html:5 | варіант | Оберіть час | Select time | Pilih masa | Pumili ng oras | Pilih waktu | Chọn giờ |
| 0574 | Бронювання / слоти | templates/booking/partials/slots.html:9 | варіант | вільно: {{ n }} | available: {{ n }} | tempat kosong: {{ n }} | bakante: {{ n }} | tersedia: {{ n }} | còn trống: {{ n }} |
| 0575 | Бронювання / слоти | templates/booking/partials/slots.html:14 | абзац | Оберіть послугу та дату, щоб побачити вільні слоти. | Select a service and date to see available slots. | Pilih perkhidmatan dan tarikh untuk melihat slot yang tersedia. | Pumili ng serbisyo at petsa para makita ang mga available na slot. | Pilih layanan dan tanggal untuk melihat slot yang tersedia. | Chọn dịch vụ và ngày để xem các khung giờ còn trống. |
| 0576 | Бронювання / слоти | templates/booking/partials/slots.html:16 | варіант | Немає слотів | No slots | Tiada slot | Walang slot | Tidak ada slot | Không có khung giờ |
| 0577 | Бронювання / models.py | apps/booking/models.py:9 | текст | Дегустація | Tasting | Pencicipan | Tasting | Pencicipan | Buổi thưởng thức |
| 0578 | Бронювання / models.py | apps/booking/models.py:10 | текст | Консультація сомельє | Sommelier consultation | Konsultasi sommelier | Konsultasyon sa sommelier | Konsultasi sommelier | Tư vấn cùng sommelier |
| 0579 | Бронювання / models.py | apps/booking/models.py:11 | текст | Візит у шоурум | Showroom visit | Lawatan ke bilik pameran | Pagbisita sa showroom | Kunjungan ke showroom | Tham quan showroom |
| 0580 | Бронювання / models.py | apps/booking/models.py:12 | текст | Самовивіз | Pickup | Ambil sendiri | Pickup | Ambil sendiri | Tự đến lấy |
| 0581 | Бронювання / повідомлення | apps/booking/views.py:55 | текст | Цей слот уже минув | This slot has already passed | Slot ini telah berlalu | Nakalipas na ang slot na ito | Slot ini sudah lewat | Khung giờ này đã qua |
| 0582 | Бронювання / повідомлення | apps/booking/views.py:171 · apps/booking/views.py:57 | текст | Немає вільних місць | No seats available | Tiada tempat kosong | Walang bakanteng upuan | Tidak ada tempat tersisa | Không còn chỗ trống |
| 0583 | Бронювання / повідомлення | apps/booking/views.py:78 | текст | Бронювання прийнято | Booking received | Tempahan diterima | Natanggap ang reserbasyon | Reservasi diterima | Đã nhận đặt lịch |
| 0584 | Бронювання / повідомлення | apps/booking/views.py:123 | текст | Слот недоступний | Slot unavailable | Slot tidak tersedia | Hindi available ang slot | Slot tidak tersedia | Khung giờ không khả dụng |
| 0585 | Бронювання / повідомлення | apps/booking/views.py:134 | текст | Бронювання прийнято. Очікуйте підтвердження. | Booking received. Please wait for confirmation. | Tempahan diterima. Sila tunggu pengesahan. | Natanggap ang reserbasyon. Hintayin ang kumpirmasyon. | Reservasi diterima. Mohon tunggu konfirmasi. | Đã nhận đặt lịch. Vui lòng chờ xác nhận. |
| 0586 | Бронювання / повідомлення | apps/booking/views.py:140 | текст | Не вдалося створити бронювання | Could not create booking | Tempahan tidak dapat dibuat | Hindi nagawa ang reserbasyon | Reservasi tidak dapat dibuat | Không thể tạo đặt lịch |
| 0587 | Бронювання / повідомлення | apps/booking/views.py:183 | текст | Бронювання прийнято. | Booking received. | Tempahan diterima. | Natanggap ang reserbasyon. | Reservasi diterima. | Đã nhận đặt lịch. |
| 0588 | Бронювання / повідомлення | apps/booking/views.py:185 | текст | Перевірте дані бронювання. | Please check your booking details. | Sila semak butiran tempahan anda. | Pakisuri ang mga detalye ng iyong reserbasyon. | Periksa data reservasi Anda. | Vui lòng kiểm tra thông tin đặt lịch. |
| 0589 | Бронювання / повідомлення | apps/booking/views.py:187 | текст | Оберіть послугу та час на сторінці бронювання. | Choose a service and time on the booking page. | Pilih perkhidmatan dan masa di halaman tempahan. | Pumili ng serbisyo at oras sa pahina ng reserbasyon. | Pilih layanan dan waktu di halaman reservasi. | Hãy chọn dịch vụ và giờ trên trang đặt lịch. |
| 0590 | Бронювання / сторінка | templates/booking/page.html:4 | текст | Бронювання | Booking | Tempahan | Reserbasyon | Reservasi | Đặt lịch |
| 0591 | Бронювання / сторінка | templates/booking/page.html:8 | h1 | Бронювання | Booking | Tempahan | Reserbasyon | Reservasi | Đặt lịch |
| 0592 | Бронювання / сторінка | templates/booking/page.html:9 | абзац | Оберіть послугу, дату та вільний слот. | Choose a service, date, and an open slot. | Pilih perkhidmatan, tarikh dan slot yang kosong. | Pumili ng serbisyo, petsa, at bakanteng slot. | Pilih layanan, tanggal, dan slot yang tersedia. | Chọn dịch vụ, ngày và khung giờ còn trống. |
| 0593 | Бронювання / сторінка | templates/booking/page.html:64 | кнопка | Забронювати | Book now | Tempah sekarang | Mag-reserve ngayon | Reservasi sekarang | Đặt lịch ngay |
| 0594 | Бронювання / послуга | apps/core/management/commands/seed_demo.py:_seed_booking | h3 | Дегустація | Tasting | Pencicipan | Tasting | Pencicipan | Buổi thưởng thức |
| 0595 | Бронювання / послуга | apps/core/management/commands/seed_demo.py:_seed_booking | h3 | Консультація сомельє | Sommelier consultation | Konsultasi sommelier | Konsultasyon sa sommelier | Konsultasi sommelier | Tư vấn cùng sommelier |
| 0596 | Бронювання / послуга | apps/core/management/commands/seed_demo.py:_seed_booking | h3 | Візит у шоурум | Showroom visit | Lawatan ke bilik pameran | Pagbisita sa showroom | Kunjungan ke showroom | Tham quan showroom |
| 0597 | Бронювання / послуга | apps/core/management/commands/seed_demo.py:_seed_booking | h3 | Самовивіз | Pickup | Ambil sendiri | Pickup | Ambil sendiri | Tự đến lấy |
| 0598 | Калькулятор / результати калькулятора | templates/calculator/partials/results.html:3 | h3 | Ваші рекомендації | Your recommendations | Cadangan untuk anda | Ang iyong mga rekomendasyon | Rekomendasi untuk Anda | Gợi ý dành cho bạn |
| 0599 | Калькулятор / результати калькулятора | templates/calculator/partials/results.html:15 | абзац | Чому підходить: {{ reasons }}. | Why it fits: {{ reasons }}. | Mengapa sesuai: {{ reasons }}. | Bakit bagay: {{ reasons }}. | Mengapa cocok: {{ reasons }}. | Vì sao phù hợp: {{ reasons }}. |
| 0600 | Калькулятор / результати калькулятора | templates/calculator/partials/results.html:20 | посилання | Переглянути | View | Lihat | Tingnan | Lihat | Xem |
| 0601 | Калькулятор / результати калькулятора | templates/calculator/partials/results.html:24 | абзац | Немає точних збігів — спробуйте інші параметри. | No exact matches — try different parameters. | Tiada padanan tepat — cuba parameter lain. | Walang eksaktong tugma — subukan ang ibang mga parameter. | Tidak ada yang cocok persis — coba parameter lain. | Không có kết quả khớp chính xác — hãy thử các tiêu chí khác. |
| 0602 | Калькулятор / services.py | apps/calculator/services.py:91 | текст | міцність %(s)s | strength %(s)s | kekuatan %(s)s | lakas na %(s)s | kekuatan %(s)s | độ mạnh %(s)s |
| 0603 | Калькулятор / services.py | apps/calculator/services.py:105 | текст | країна %(c)s | country %(c)s | negara %(c)s | bansang %(c)s | negara %(c)s | quốc gia %(c)s |
| 0604 | Калькулятор / services.py | apps/calculator/services.py:120 | текст | формат %(f)s | format %(f)s | saiz %(f)s | sukat na %(f)s | ukuran %(f)s | kích cỡ %(f)s |
| 0605 | Калькулятор / services.py | apps/calculator/services.py:127 | текст | у бюджеті (%(p)s %(symbol)s) | within budget (%(p)s %(symbol)s) | dalam bajet (%(p)s %(symbol)s) | pasok sa badyet (%(p)s %(symbol)s) | sesuai anggaran (%(p)s %(symbol)s) | trong ngân sách (%(p)s %(symbol)s) |
| 0606 | Калькулятор / services.py | apps/calculator/services.py:136 | текст | близький за профілем асортименту | close to your preferred profile | hampir menyerupai profil pilihan anda | malapit sa gusto mong profile | mendekati profil yang Anda sukai | gần với hương vị bạn ưa thích |
| 0607 | Калькулятор / models.py | apps/calculator/models.py:13 | текст | Міцність | Strength | Kekuatan | Lakas | Kekuatan | Độ mạnh |
| 0608 | Калькулятор / models.py | apps/calculator/models.py:14 | текст | Формат | Format | Saiz | Sukat | Ukuran | Kích cỡ |
| 0609 | Калькулятор / models.py | apps/calculator/models.py:15 | текст | Країна | Country | Negara | Bansa | Negara | Quốc gia |
| 0610 | Калькулятор / models.py | apps/calculator/models.py:16 | текст | Бюджет | Budget | Bajet | Badyet | Anggaran | Ngân sách |
| 0611 | Калькулятор / Міцність | apps/core/management/commands/seed_demo.py:calculator.strength | h2 | Міцність | Strength | Kekuatan | Lakas | Kekuatan | Độ mạnh |
| 0612 | Калькулятор / Міцність | apps/core/management/commands/seed_demo.py:calculator.strength | варіант | Легка | Mild | Ringan | Banayad | Ringan | Nhẹ |
| 0613 | Калькулятор / Міцність | apps/core/management/commands/seed_demo.py:calculator.strength | варіант | Середня | Medium | Sederhana | Katamtaman | Sedang | Vừa |
| 0614 | Калькулятор / Міцність | apps/core/management/commands/seed_demo.py:calculator.strength | варіант | Середньо-повна | Medium-full | Sederhana-penuh | Katamtaman hanggang malakas | Sedang-penuh | Vừa đến đậm |
| 0615 | Калькулятор / Міцність | apps/core/management/commands/seed_demo.py:calculator.strength | варіант | Повна | Full | Penuh | Malakas | Penuh | Đậm |
| 0616 | Калькулятор / Формат | apps/core/management/commands/seed_demo.py:calculator.format | h2 | Формат | Format | Saiz | Sukat | Ukuran | Kích cỡ |
| 0617 | Калькулятор / Формат | apps/core/management/commands/seed_demo.py:calculator.format | варіант | Petit Robusto | Petit Robusto | Petit Robusto | Petit Robusto | Petit Robusto | Petit Robusto |
| 0618 | Калькулятор / Формат | apps/core/management/commands/seed_demo.py:calculator.format | варіант | Robusto | Robusto | Robusto | Robusto | Robusto | Robusto |
| 0619 | Калькулятор / Формат | apps/core/management/commands/seed_demo.py:calculator.format | варіант | Toro | Toro | Toro | Toro | Toro | Toro |
| 0620 | Калькулятор / Формат | apps/core/management/commands/seed_demo.py:calculator.format | варіант | Churchill | Churchill | Churchill | Churchill | Churchill | Churchill |
| 0621 | Калькулятор / Країна | apps/core/management/commands/seed_demo.py:calculator.country | h2 | Країна | Country | Negara | Bansa | Negara | Quốc gia |
| 0622 | Калькулятор / Країна | apps/core/management/commands/seed_demo.py:calculator.country | варіант | Куба | Cuba | Cuba | Cuba | Kuba | Cuba |
| 0623 | Калькулятор / Країна | apps/core/management/commands/seed_demo.py:calculator.country | варіант | Нікарагуа | Nicaragua | Nicaragua | Nicaragua | Nikaragua | Nicaragua |
| 0624 | Калькулятор / Країна | apps/core/management/commands/seed_demo.py:calculator.country | варіант | Домінікана | Dominican Republic | Republik Dominican | Dominican Republic | Republik Dominika | Cộng hòa Dominica |
| 0625 | Калькулятор / Країна | apps/core/management/commands/seed_demo.py:calculator.country | варіант | Будь-яка | Any | Mana-mana | Alinman | Mana saja | Bất kỳ |
| 0626 | Калькулятор / Бюджет | apps/core/management/commands/seed_demo.py:calculator.budget | h2 | Бюджет | Budget | Bajet | Badyet | Anggaran | Ngân sách |
| 0627 | Калькулятор / Бюджет | apps/core/management/commands/seed_demo.py:calculator.budget | варіант | до 1000 ₴ | up to 1000 ₴ | sehingga 1000 ₴ | hanggang 1000 ₴ | hingga 1000 ₴ | đến 1000 ₴ |
| 0628 | Калькулятор / Бюджет | apps/core/management/commands/seed_demo.py:calculator.budget | варіант | без обмежень | no limit | tanpa had | walang limitasyon | tanpa batasan | không giới hạn |
| 0629 | Контакти / контакти | templates/leads/contact.html:12 | підпис | Імʼя | First name | Nama | Pangalan | Nama | Tên |
| 0630 | Контакти / контакти | templates/leads/contact.html:13 | підпис | Email | Email | E-mel | Email | Email | Email |
| 0631 | Контакти / контакти | templates/leads/contact.html:14 | підпис | Телефон | Phone | Telefon | Telepono | Telepon | Số điện thoại |
| 0632 | Контакти / контакти | templates/leads/contact.html:15 | підпис | Повідомлення | Message | Mesej | Mensahe | Pesan | Tin nhắn |
| 0633 | Контакти / контакти | templates/leads/contact.html:16 | підпис | Пн–Нд: 11:00–21:00 | Mon–Sun: 11:00–21:00 | Isn–Ahd: 11:00–21:00 | Lun–Lin: 11:00–21:00 | Sen–Min: 11:00–21:00 | T2–CN: 11:00–21:00 |
| 0634 | Контакти / контакти | templates/leads/contact.html:20 | aria-label | Контактна інформація | Contact information | Maklumat hubungan | Impormasyon sa pakikipag-ugnayan | Informasi kontak | Thông tin liên hệ |
| 0635 | Контакти / контакти | templates/leads/contact.html:30 | підпис | Телефон | Phone | Telefon | Telepono | Telepon | Số điện thoại |
| 0636 | Контакти / контакти | templates/leads/contact.html:42 | підпис | Адреса | Address | Alamat | Address | Alamat | Địa chỉ |
| 0637 | Контакти / контакти | templates/leads/contact.html:46 | підпис | Години | Hours | Waktu operasi | Oras ng bukas | Jam buka | Giờ mở cửa |
| 0638 | Контакти / повідомлення | apps/leads/views.py:31 | текст | Вкажіть телефон або email | Enter a phone number or email | Masukkan nombor telefon atau e-mel | Maglagay ng numero ng telepono o email | Masukkan nomor telepon atau email | Vui lòng nhập số điện thoại hoặc email |
| 0639 | Контакти / повідомлення | apps/leads/views.py:72 | текст | Запит надіслано. Менеджер звʼяжеться з вами. | Request sent. A manager will contact you. | Permintaan dihantar. Pengurus akan menghubungi anda. | Naipadala na ang kahilingan. Makikipag-ugnayan sa iyo ang manager. | Permintaan terkirim. Manajer akan menghubungi Anda. | Đã gửi yêu cầu. Quản lý sẽ liên hệ với bạn. |
| 0640 | Контакти / повідомлення | apps/leads/views.py:100 | текст | Повідомлення надіслано. | Message sent. | Mesej dihantar. | Naipadala na ang mensahe. | Pesan terkirim. | Đã gửi tin nhắn. |
| 0641 | Контакти / повідомлення | apps/leads/views.py:118 | текст | Дякуємо! Передзвонимо найближчим часом. | Thank you! We will call you back shortly. | Terima kasih! Kami akan menelefon anda semula tidak lama lagi. | Salamat! Tatawagan ka namin sa lalong madaling panahon. | Terima kasih! Kami akan segera menelepon Anda kembali. | Cảm ơn bạn! Chúng tôi sẽ sớm gọi lại cho bạn. |
| 0642 | Контакти / повідомлення | apps/leads/views.py:120 | текст | Заявку прийнято | Request received | Permintaan diterima | Natanggap ang kahilingan | Permintaan diterima | Đã nhận yêu cầu |
| 0643 | Контакти / повідомлення | apps/leads/views.py:123 · apps/leads/views.py:127 | текст | Перевірте номер телефону. | Please check your phone number. | Sila semak nombor telefon anda. | Pakisuri ang iyong numero ng telepono. | Periksa nomor telepon Anda. | Vui lòng kiểm tra số điện thoại. |
| 0644 | Контакти / контакти | templates/leads/contact.html:53 | абзац | Контакти | Contacts | Hubungi kami | Makipag-ugnayan | Kontak | Liên hệ |
| 0645 | Контакти / контакти | templates/leads/contact.html:4 | текст | Напишіть нам | Write to us | Hantar mesej kepada kami | Sumulat sa amin | Kirim pesan kepada kami | Nhắn tin cho chúng tôi |
| 0646 | Контакти / контакти | templates/leads/contact.html:54 | h1 | Напишіть нам | Write to us | Hantar mesej kepada kami | Sumulat sa amin | Kirim pesan kepada kami | Nhắn tin cho chúng tôi |
| 0647 | Контакти / контакти | templates/leads/contact.html:55 | абзац | Відповідаємо протягом робочого дня. | We reply during business hours. | Kami membalas pada waktu bekerja. | Sumasagot kami sa loob ng oras ng trabaho. | Kami membalas pada jam kerja. | Chúng tôi phản hồi trong giờ làm việc. |
| 0648 | Контакти / контакти | templates/leads/contact.html:25 | текст | Карта — Хрещатик 1 | Map — Khreshchatyk 1 | Peta — Khreshchatyk 1 | Mapa — Khreshchatyk 1 | Peta — Khreshchatyk 1 | Bản đồ — Khreshchatyk 1 |
| 0649 | Контакти / контакти | templates/leads/contact.html:64 | кнопка | Надіслати | Send | Hantar | Ipadala | Kirim | Gửi |
| 0650 | Контакти / контакти | templates/leads/contact.html:65 | кнопка | Замовити дзвінок | Request a call | Minta panggilan balik | Humiling ng tawag | Minta dihubungi | Yêu cầu gọi lại |
| 0651 | B2B / B2B | templates/leads/b2b.html:7 | підпис | Контактна особа | Contact person | Orang untuk dihubungi | Contact person | Narahubung | Người liên hệ |
| 0652 | B2B / B2B | templates/leads/b2b.html:8 | підпис | Телефон | Phone | Telefon | Telepono | Telepon | Số điện thoại |
| 0653 | B2B / B2B | templates/leads/b2b.html:9 | підпис | Email | Email | E-mel | Email | Email | Email |
| 0654 | B2B / B2B | templates/leads/b2b.html:10 | підпис | Що цікавить | What are you interested in | Apa yang anda minati | Ano ang interes mo | Apa yang Anda minati | Bạn quan tâm đến điều gì |
| 0655 | B2B / B2B | templates/leads/b2b.html:11 | підпис | Прайс, гравіювання, корпоративні набори… | Pricing, engraving, corporate sets… | Senarai harga, ukiran, set korporat… | Listahan ng presyo, pag-ukit, mga corporate set… | Daftar harga, ukiran, paket korporat… | Bảng giá, khắc chữ, bộ quà doanh nghiệp… |
| 0656 | B2B / B2B | templates/leads/b2b.html:21 | підпис | Компанія | Company | Syarikat | Kompanya | Perusahaan | Công ty |
| 0657 | B2B / B2B | templates/leads/b2b.html:4 | текст | B2B | B2B | B2B | B2B | B2B | B2B |
| 0658 | B2B / B2B | templates/leads/b2b.html:13 | h1 | B2B | B2B | B2B | B2B | B2B | B2B |
| 0659 | B2B / B2B | templates/leads/b2b.html:14 | абзац | Прайс і умови для барів, готелів і корпоративних подарунків. | Pricing and terms for bars, hotels, and corporate gifts. | Senarai harga dan terma untuk bar, hotel dan hadiah korporat. | Presyo at mga tuntunin para sa mga bar, hotel, at corporate gift. | Daftar harga dan ketentuan untuk bar, hotel, dan hadiah korporat. | Bảng giá và điều khoản dành cho quán bar, khách sạn và quà tặng doanh nghiệp. |
| 0660 | B2B / B2B | templates/leads/b2b.html:30 | кнопка | Запросити прайс | Request a price list | Minta senarai harga | Humiling ng listahan ng presyo | Minta daftar harga | Yêu cầu bảng giá |
