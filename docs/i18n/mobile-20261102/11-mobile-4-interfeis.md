# Мобільний застосунок — інтерфейс

Підписи, яких немає в seed: таби, форми, порожні стани, запасні рядки екранів.

Переклади English, 中文 (zh-hans), ms, fil, id, vi заповнені. Українська колонка — джерело.

Статуси: `оригінал` — текст не перекладається, у колонках мов лишається оригінал; `переклад` — підпис інтерфейсу, терміни узгоджені з вітриною; `чернетка` — потребує людського рев'ю перед публікацією (юридичні тексти, вікові формулювання, історії та факти брендів).

M116–M118: у формі візиту одне поле імені, тому English і 中文 мають «Name» і «姓名», а не «First name» з реєстрації на сайті.

Один рядок — одна фраза, заголовок, підпис або абзац. Однаковий український текст має один ID.

Дія `перекласти` означає, що шість колонок треба заповнити окремим проходом. Дія `не перекладати` означає, що в застосунку лишається цей оригінал: назва, лінійка, вордмарк, маска або номер.

Плейсхолдер `{date}` лишається в перекладі на тому самому місці. Імена людей і топоніми всередині фрази не замінювати іншими назвами.

| ID | Де | Адреса | Роль | Дія | Українською | English | 中文 (zh-hans) | ms | fil | id | vi | Статус |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M114 | Ще / kicker · назва застосунку | mobile/lib/app.dart:18 · mobile/lib/features/more/presentation/more_screen.dart:26 · mobile/lib/features/more/presentation/more_screen.dart:111 · mobile/ios/Runner/Info.plist:8 · mobile/android/app/src/main/AndroidManifest.xml:4 · mobile/web/index.html:32 · mobile/web/manifest.json:2 | вордмарк | не перекладати | Royal Smoke | Royal Smoke | Royal Smoke | Royal Smoke | Royal Smoke | Royal Smoke | Royal Smoke | оригінал |
| M115 | Вік / запасний абзац екрана | mobile/lib/features/age_gate/presentation/age_gate_screen.dart:85 | абзац | перекласти | Застосунок є інформаційним довідником брендів. | The app is an informational guide to brands. | 本应用是品牌信息指南。 | Aplikasi ini ialah panduan maklumat tentang jenama. | Ang app ay isang gabay ng impormasyon tungkol sa mga brand. | Aplikasi ini adalah panduan informasi tentang merek. | Ứng dụng là cẩm nang thông tin về các thương hiệu. | чернетка |
| M116 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:114 | мітка | перекласти | Імʼя | Name | 姓名 | Nama | Pangalan | Nama | Tên | переклад |
| M117 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:115 | плейсхолдер | перекласти | Ваше імʼя | Your name | 您的姓名 | Nama anda | Ang iyong pangalan | Nama Anda | Tên của bạn | переклад |
| M118 | Візит / помилка | mobile/lib/features/booking/presentation/visit_screen.dart:117 · mobile/lib/features/booking/presentation/visit_screen.dart:126 | помилка | перекласти | Вкажіть імʼя та телефон | Enter your name and phone number | 请填写姓名和电话 | Sila masukkan nama dan nombor telefon | Ilagay ang iyong pangalan at numero ng telepono | Masukkan nama dan nomor telepon | Vui lòng nhập tên và số điện thoại | переклад |
| M119 | Контакти / мітка | mobile/lib/features/booking/presentation/visit_screen.dart:122 · mobile/lib/features/contacts/presentation/contacts_screen.dart:64 | мітка | перекласти | Телефон | Phone | 电话 | Telefon | Telepono | Telepon | Số điện thoại | переклад |
| M120 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:123 | маска | не перекладати | +380 | +380 | +380 | +380 | +380 | +380 | +380 | оригінал |
| M121 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:132 | мітка | перекласти | Дата | Date | 日期 | Tarikh | Petsa | Tanggal | Ngày | переклад |
| M122 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:132 | маска | перекласти | ДД.ММ.РРРР | DD.MM.YYYY | 日.月.年 | HH.BB.TTTT | DD.MM.YYYY | DD.MM.YYYY | NN.TT.NNNN | переклад |
| M123 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:134 | мітка | перекласти | Час | Time | 时间 | Masa | Oras | Waktu | Giờ | переклад |
| M124 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:134 | маска | перекласти | ГГ:ХХ | HH:MM | 时:分 | JJ:MM | HH:MM | JJ:MM | GG:PP | переклад |
| M125 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:138 | мітка | перекласти | Коментар | Comment | 备注 | Catatan | Komento | Catatan | Ghi chú | переклад |
| M126 | Візит / поле | mobile/lib/features/booking/presentation/visit_screen.dart:138 | плейсхолдер | перекласти | Необовʼязково | Optional | 选填 | Pilihan | Opsyonal | Opsional | Không bắt buộc | переклад |
| M127 | Бренд / помилка | mobile/lib/features/brands/presentation/brand_detail_screen.dart:26 | заголовок | перекласти | Бренд не знайдено | Brand not found | 未找到该品牌 | Jenama tidak ditemui | Hindi nahanap ang brand | Merek tidak ditemukan | Không tìm thấy thương hiệu | переклад |
| M128 | Бренд / візерунок | mobile/lib/features/brands/presentation/brand_detail_screen.dart:40 | вордмарк | не перекладати | ROYAL | ROYAL | ROYAL | ROYAL | ROYAL | ROYAL | ROYAL | оригінал |
| M129 | Бренд / назад | mobile/lib/features/brands/presentation/brand_detail_screen.dart:60 | кнопка | перекласти | БРЕНДИ | BRANDS | 品牌 | JENAMA | MGA BRAND | MEREK | THƯƠNG HIỆU | переклад |
| M130 | Бренд / kicker фактів | mobile/lib/features/brands/presentation/brand_detail_screen.dart:112 | kicker | перекласти | КОРОТКО | IN BRIEF | 概览 | RINGKASAN | BUOD | RINGKASAN | TÓM TẮT | переклад |
| M131 | Бренд / kicker лінійок | mobile/lib/features/brands/presentation/brand_detail_screen.dart:124 | kicker | перекласти | ЛІНІЙКИ | LINES | 系列 | BARISAN PRODUK | MGA LINYA | LINI PRODUK | DÒNG SẢN PHẨM | переклад |
| M132 | Бренд / посилання | mobile/lib/features/brands/presentation/brand_detail_screen.dart:131 | кнопка | перекласти | УСІ БРЕНДИ | ALL BRANDS | 全部品牌 | SEMUA JENAMA | LAHAT NG BRAND | SEMUA MEREK | TẤT CẢ THƯƠNG HIỆU | переклад |
| M133 | Бренди / kicker | mobile/lib/features/brands/presentation/brands_screen.dart:43 | kicker | перекласти | Партнери дому | Partners of the house | 品牌之家的合作伙伴 | Rakan kongsi rumah | Mga katuwang ng bahay | Mitra rumah | Đối tác của ngôi nhà | переклад |
| M134 | Бренди / фільтр | mobile/lib/features/brands/presentation/brands_screen.dart:47 | чип | перекласти | Усі | All | 全部 | Semua | Lahat | Semua | Tất cả | переклад |
| M135 | Ще / заголовок | mobile/lib/features/contacts/presentation/contacts_screen.dart:37 · mobile/lib/features/more/presentation/more_screen.dart:26 · mobile/lib/features/more/presentation/more_screen.dart:101 · mobile/lib/shared/widgets/rs_chrome.dart:256 | заголовок | перекласти | Ще | More | 更多 | Lagi | Higit pa | Lainnya | Thêm | переклад |
| M136 | Контакти / мітка | mobile/lib/features/contacts/presentation/contacts_screen.dart:54 | мітка | перекласти | Адреса | Address | 地址 | Alamat | Address | Alamat | Địa chỉ | переклад |
| M137 | Контакти / дія | mobile/lib/features/contacts/presentation/contacts_screen.dart:56 | кнопка | перекласти | Прокласти маршрут | Get directions | 规划路线 | Dapatkan arah | Kumuha ng direksyon | Petunjuk arah | Chỉ đường | переклад |
| M138 | Контакти / дія | mobile/lib/features/contacts/presentation/contacts_screen.dart:66 | кнопка | перекласти | Зателефонувати | Call | 拨打电话 | Buat panggilan | Tumawag | Telepon | Gọi điện | переклад |
| M139 | Контакти / мітка | mobile/lib/features/contacts/presentation/contacts_screen.dart:69 | мітка | перекласти | Години | Hours | 营业时间 | Waktu operasi | Oras ng bukas | Jam buka | Giờ mở cửa | переклад |
| M140 | Головна / kicker блоку | mobile/lib/features/home/presentation/home_screen.dart:98 | kicker | перекласти | ПАРТНЕРИ | PARTNERS | 合作伙伴 | RAKAN KONGSI | MGA KATUWANG | MITRA | ĐỐI TÁC | переклад |
| M141 | Дім / запасний абзац екрана | mobile/lib/features/house/presentation/house_screen.dart:30 | абзац | перекласти | Royal Smoke — дім, що представляє в Україні родинні бренди з багаторічною історією. | Royal Smoke is a house that represents family brands with a long history in Ukraine. | Royal Smoke 是一座品牌之家，在乌克兰代理历史悠久的家族品牌。 | Royal Smoke ialah rumah yang mewakili jenama keluarga yang mempunyai sejarah panjang di Ukraine. | Ang Royal Smoke ay isang bahay na kumakatawan sa mga brand ng pamilya na may mahabang kasaysayan sa Ukraine. | Royal Smoke adalah rumah yang mewakili merek-merek keluarga dengan sejarah panjang di Ukraina. | Royal Smoke là ngôi nhà đại diện cho các thương hiệu gia đình có lịch sử lâu đời tại Ukraine. | переклад |
| M142 | Ще / пункт | mobile/lib/features/more/presentation/more_screen.dart:30 | пункт | перекласти | Збережені бренди | Saved brands | 已保存的品牌 | Jenama tersimpan | Mga naka-save na brand | Merek tersimpan | Thương hiệu đã lưu | переклад |
| M143 | Ще / запасний заголовок | mobile/lib/features/more/presentation/more_screen.dart:86 | заголовок | перекласти | Документ | Document | 文档 | Dokumen | Dokumento | Dokumen | Tài liệu | переклад |
| M144 | Офлайн / статус | mobile/lib/features/offline/presentation/offline_screen.dart:26 | підпис | перекласти | Локальний каталог | Local catalog | 本地目录 | Katalog setempat | Lokal na katalogo | Katalog lokal | Danh mục cục bộ | переклад |
| M145 | Офлайн / статус | mobile/lib/features/offline/presentation/offline_screen.dart:26 | підпис | перекласти | Оновлено {date} | Updated {date} | 更新于 {date} | Dikemas kini {date} | Na-update noong {date} | Diperbarui {date} | Đã cập nhật {date} | переклад |
| M146 | Офлайн / kicker | mobile/lib/features/offline/presentation/offline_screen.dart:31 | kicker | перекласти | Довідник | Guide | 指南 | Panduan | Gabay | Panduan | Cẩm nang | переклад |
| M147 | Офлайн / заголовок | mobile/lib/features/offline/presentation/offline_screen.dart:32 · mobile/lib/shared/widgets/rs_chrome.dart:255 | заголовок | перекласти | Офлайн | Offline | 离线 | Luar talian | Offline | Offline | Ngoại tuyến | переклад |
| M148 | Офлайн / підзаголовок | mobile/lib/features/offline/presentation/offline_screen.dart:33 | підзаголовок | перекласти | Збережений довідник брендів | Saved brand guide | 已保存的品牌指南 | Panduan jenama tersimpan | Naka-save na gabay sa mga brand | Panduan merek tersimpan | Cẩm nang thương hiệu đã lưu | переклад |
| M149 | Офлайн / порожній стан | mobile/lib/features/offline/presentation/offline_screen.dart:59 | абзац | перекласти | Поки немає збережених брендів.\nДодайте їх закладкою на картці бренду. | No saved brands yet.\nAdd them with the bookmark on a brand card. | 暂无已保存的品牌。\n请点击品牌卡片上的书签进行添加。 | Belum ada jenama tersimpan.\nTambahkannya dengan penanda halaman pada kad jenama. | Wala pang naka-save na brand.\nIdagdag ang mga ito gamit ang bookmark sa card ng brand. | Belum ada merek tersimpan.\nTambahkan dengan penanda pada kartu merek. | Chưa có thương hiệu nào được lưu.\nHãy thêm bằng dấu trang trên thẻ thương hiệu. | переклад |
| M150 | Бренд / закладка | mobile/lib/shared/widgets/rs_brand.dart:200 | підпис | перекласти | ЗБЕРЕЖЕНО | SAVED | 已保存 | TERSIMPAN | NAKA-SAVE | TERSIMPAN | ĐÃ LƯU | переклад |
| M151 | Порожній стан / монограма | mobile/lib/shared/widgets/rs_brand_pattern.dart:26 · mobile/lib/shared/widgets/rs_chrome.dart:156 · mobile/lib/shared/widgets/rs_chrome.dart:196 | монограма | не перекладати | RS | RS | RS | RS | RS | RS | RS | оригінал |
| M152 | Бренди / порожній пошук | mobile/lib/shared/widgets/rs_chrome.dart:206 | заголовок | перекласти | Нічого не знайдено | Nothing found | 未找到结果 | Tiada hasil dijumpai | Walang natagpuan | Tidak ada hasil | Không tìm thấy kết quả | переклад |
| M153 | Бренди / порожній пошук | mobile/lib/shared/widgets/rs_chrome.dart:208 | абзац | перекласти | Спробуйте іншу назву | Try a different name | 请尝试其他名称 | Cuba nama lain | Subukan ang ibang pangalan | Coba nama lain | Hãy thử tên khác | переклад |
| M154 | Офлайн / чип | mobile/lib/shared/widgets/rs_chrome.dart:236 | чип | перекласти | ОФЛАЙН-РЕЖИМ | OFFLINE MODE | 离线模式 | MOD LUAR TALIAN | OFFLINE MODE | MODE OFFLINE | CHẾ ĐỘ NGOẠI TUYẾN | переклад |
| M155 | Навігація / таб | mobile/lib/shared/widgets/rs_chrome.dart:252 | таб | перекласти | Головна | Home | 首页 | Laman utama | Home | Beranda | Trang chủ | переклад |
| M156 | Бренди / пошук | mobile/lib/shared/widgets/rs_fields.dart:99 | плейсхолдер | перекласти | Пошук бренду | Search brand | 搜索品牌 | Cari jenama | Maghanap ng brand | Cari merek | Tìm thương hiệu | переклад |
| M157 | Контакти / мапа | mobile/lib/shared/widgets/rs_venue_map.dart:61 | підпис | перекласти | МАПА | MAP | 地图 | PETA | MAPA | PETA | BẢN ĐỒ | переклад |
| M158 | Пакет / опис | mobile/pubspec.yaml:2 | абзац | перекласти | Royal Smoke — довідник бренду. | Royal Smoke — brand guide. | Royal Smoke — 品牌指南。 | Royal Smoke — panduan jenama. | Royal Smoke — gabay sa brand. | Royal Smoke — panduan merek. | Royal Smoke — cẩm nang thương hiệu. | переклад |
| M159 | Веб-версія / опис | mobile/web/index.html:21 · mobile/web/manifest.json:8 | абзац | перекласти | Довідник бренду Royal Smoke. | Royal Smoke brand guide. | Royal Smoke 品牌指南。 | Panduan jenama Royal Smoke. | Gabay sa brand ng Royal Smoke. | Panduan merek Royal Smoke. | Cẩm nang thương hiệu Royal Smoke. | переклад |

Фраз у файлі: 46. До перекладу: 42. Оригінал без перекладу: 4.
