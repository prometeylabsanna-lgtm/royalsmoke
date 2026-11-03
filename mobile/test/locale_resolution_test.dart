import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/core/l10n/locale_resolution.dart';

void main() {
  const en = Locale('en');
  const uk = Locale('uk');
  const zhHans = Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans');

  test('de → en', () {
    expect(resolveAppLocale(deviceLocale: const Locale('de')), en);
  });

  test('uk-UA → uk', () {
    expect(resolveAppLocale(deviceLocale: const Locale('uk', 'UA')), uk);
  });

  test('en-GB → en', () {
    expect(resolveAppLocale(deviceLocale: const Locale('en', 'GB')), en);
  });

  test('zh-Hans-CN → zh_Hans', () {
    expect(
      resolveAppLocale(
        deviceLocale: const Locale.fromSubtags(
          languageCode: 'zh',
          scriptCode: 'Hans',
          countryCode: 'CN',
        ),
      ),
      zhHans,
    );
  });

  test('zh-CN і голий zh → zh_Hans', () {
    expect(resolveAppLocale(deviceLocale: const Locale('zh', 'CN')), zhHans);
    expect(resolveAppLocale(deviceLocale: const Locale('zh')), zhHans);
    expect(
      resolveAppLocale(
        savedCode: 'zh-Hans-CN',
        deviceLocale: const Locale('de'),
      ),
      zhHans,
    );
    expect(
      resolveAppLocale(
        savedCode: 'zh_Hans_CN',
        deviceLocale: const Locale('de'),
      ),
      zhHans,
    );
  });

  test('zh-Hant і zh-TW → en, не uk', () {
    expect(resolveAppLocale(deviceLocale: const Locale('zh', 'TW')), en);
    expect(resolveAppLocale(deviceLocale: const Locale('zh', 'HK')), en);
    expect(
      resolveAppLocale(
        deviceLocale: const Locale.fromSubtags(
          languageCode: 'zh',
          scriptCode: 'Hant',
          countryCode: 'TW',
        ),
      ),
      en,
    );
  });

  test('fil-PH → fil, id-ID → id, ms-MY і vi-VN', () {
    expect(
      resolveAppLocale(deviceLocale: const Locale('fil', 'PH')),
      const Locale('fil'),
    );
    expect(
      resolveAppLocale(deviceLocale: const Locale('id', 'ID')),
      const Locale('id'),
    );
    expect(
      resolveAppLocale(deviceLocale: const Locale('ms', 'MY')),
      const Locale('ms'),
    );
    expect(
      resolveAppLocale(deviceLocale: const Locale('vi', 'VN')),
      const Locale('vi'),
    );
  });

  test('застарілі in і tl', () {
    expect(
      resolveAppLocale(deviceLocale: const Locale('in')),
      const Locale('id'),
    );
    expect(
      resolveAppLocale(deviceLocale: const Locale('in', 'ID')),
      const Locale('id'),
    );
    expect(
      resolveAppLocale(deviceLocale: const Locale('tl')),
      const Locale('fil'),
    );
    expect(
      resolveAppLocale(deviceLocale: const Locale('tl', 'PH')),
      const Locale('fil'),
    );
    expect(
      resolveAppLocale(savedCode: 'in', deviceLocale: const Locale('de')),
      const Locale('id'),
    );
    expect(
      resolveAppLocale(savedCode: 'tl', deviceLocale: const Locale('de')),
      const Locale('fil'),
    );
  });

  test('збережений вибір перекриває мову пристрою', () {
    expect(
      resolveAppLocale(savedCode: 'uk', deviceLocale: const Locale('de')),
      uk,
    );
    expect(
      resolveAppLocale(savedCode: 'en', deviceLocale: const Locale('uk', 'UA')),
      en,
    );
    expect(
      resolveAppLocale(savedCode: 'zh-hans', deviceLocale: const Locale('de')),
      zhHans,
    );
    expect(
      resolveAppLocale(savedCode: ' EN ', deviceLocale: const Locale('uk')),
      en,
    );
  });

  test('порожній або невідомий вибір падає на пристрій, інакше на en', () {
    expect(
      resolveAppLocale(savedCode: null, deviceLocale: const Locale('uk', 'UA')),
      uk,
    );
    expect(
      resolveAppLocale(
        savedCode: '   ',
        deviceLocale: const Locale('vi', 'VN'),
      ),
      const Locale('vi'),
    );
    expect(
      resolveAppLocale(savedCode: 'fr', deviceLocale: const Locale('id', 'ID')),
      const Locale('id'),
    );
    expect(
      resolveAppLocale(savedCode: 'de', deviceLocale: const Locale('fr')),
      en,
    );
    expect(localeFromCode('de'), en);
    expect(matchDeviceLocale(const Locale('de')), en);
  });
}
