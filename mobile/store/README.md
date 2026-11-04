# RoyalSmoke — матеріали для сторів

Тексти лежать у `metadata/<locale>/`. Назва в `name.txt` скрізь `RoyalSmoke`.
Факти лише з застосунку та прод-бандла: дім бренду, партнери AJ Fernandez, Oliva, Perdomo, Casa Turrent, запис на візит, контакти в Києві (вул. Хрещатик, 1; Пн–Нд 11:00–22:00), підтвердження 21+.
Окремого розділу подій у застосунку немає, тож у текстах його немає. PDR і Praha в поточному бандлі відсутні.

## Чеклист перед відправкою

- Android: `app-release.aab` підписаний upload-ключем (сертифікат CN=RoyalSmoke, не Android Debug). `key.properties` не комітити.
- У release-маніфесті немає `usesCleartextTraffic`. Debug і profile лишають cleartext для локального API.
- iOS: `PrivacyInfo.xcprivacy` у Copy Bundle Resources. Трекінгу немає. `shared_preferences` пише лише на пристрій (мова, кеш довідника, збережені бренди) через UserDefaults.
- Форма візиту в цій збірці не відправляє дані на сервер: після валідації показує локальне підтвердження. В анкетах App Privacy / Data safety не позначайте збір імені чи телефону, доки це не зміниться в коді.
- Віковий рейтинг: 18+ / 21. Не вказуйте продаж і не давайте посилань на продаж.
- Експортне шифрування: лише стандартний HTTPS.
- Публічний URL політики додайте в консолі лише якщо така сторінка вже є. Текст політики є в застосунку, розділ «Ще».

## Скріншоти

Каталоги: `screenshots/ios-6.9/`, `screenshots/ios-6.5/`, `screenshots/android-phone/`.

App Store, портрет, без альфа-каналу:

- 6.9" (iPhone 17 Pro Max / 16 Pro Max): 1320×2868, 1290×2796 або 1260×2736 px.
- 6.5" (iPhone 11 Pro Max / XS Max): 1284×2778 або 1242×2688 px.
- 3–10 кадрів на розмір. Статус-бар: 9:41, без чужих банерів.

Google Play, телефон:

- мінімум 2, максимум 8;
- JPEG або 24-bit PNG без альфа;
- кожна сторона від 320 до 3840 px, співвідношення не гостріше за 2:1;
- зручно здавати 9:16, наприклад 1080×1920.

Кадри: вікове підтвердження, головна, бренди, картка бренду, запис на візит, контакти. На зображеннях не має бути заборонених формулювань.

## App Store 1.4.3

Джерело: https://developer.apple.com/app-store/review/guidelines/#1.4.3

> Apps that encourage consumption of tobacco and vape products, illegal drugs, or excessive amounts of alcohol are not permitted. Apps that encourage minors to consume any of these substances will be rejected. Facilitating the sale of controlled substances (except for licensed pharmacies and licensed or otherwise legal cannabis dispensaries), or tobacco is not allowed.

## Google Play

Джерело: https://support.google.com/googleplay/android-developer/answer/9878810

> Tobacco and Alcohol
>
> Apps that facilitate the sale of tobacco or products containing nicotine (such as e-cigarettes, vape pens and nicotine pouches) or encourage the illegal or inappropriate use of alcohol, tobacco, or nicotine are not allowed.

Не зображуйте й не заохочуйте вживання неповнолітніми. Не рекламуйте такі товари і не ведіть на сайти продажу. Обмежений виняток для доставки продуктів у окремих регіонах до цього застосунку не стосується: продажу в застосунку немає.
