import 'dart:ui';

/// Запасна мова, якщо збережений вибір і локаль пристрою не підтримані.
const fallbackLocale = Locale('en');

const _supported = <String>{'uk', 'en', 'ms', 'fil', 'id', 'vi'};

/// Порядок: збережений вибір → локаль пристрою, якщо вона підтримана → англійська.
///
/// Підтримані мови: uk, en, zh_Hans, ms, fil, id, vi.
/// Враховує скрипт і регіон (`zh-Hans-CN`, `zh-CN`, `en-GB`, `fil-PH`, `id-ID`, `uk-UA`),
/// а також застарілі коди `in` (індонезійська) і `tl` (філіппінська).
Locale resolveAppLocale({String? savedCode, required Locale deviceLocale}) {
  final saved = _localeFromTag(savedCode);
  if (saved != null) return saved;
  return _localeFromTag(_tagOf(deviceLocale)) ?? fallbackLocale;
}

/// Код з перемикача або кешу. Невідомий код → [fallbackLocale].
Locale localeFromCode(String code) => _localeFromTag(code) ?? fallbackLocale;

/// Лише локаль пристрою, без збереженого вибору.
Locale matchDeviceLocale(Locale device) =>
    resolveAppLocale(deviceLocale: device);

String _tagOf(Locale locale) {
  final buffer = StringBuffer(locale.languageCode);
  final script = locale.scriptCode;
  final region = locale.countryCode;
  if (script != null && script.isNotEmpty) {
    buffer
      ..write('-')
      ..write(script);
  }
  if (region != null && region.isNotEmpty) {
    buffer
      ..write('-')
      ..write(region);
  }
  return buffer.toString();
}

Locale? _localeFromTag(String? raw) {
  if (raw == null) return null;
  final code = raw.trim().toLowerCase().replaceAll('_', '-');
  if (code.isEmpty) return null;

  final parts = code.split('-').where((part) => part.isNotEmpty).toList();
  if (parts.isEmpty) return null;

  final language = parts.first;
  var script = '';
  var region = '';
  if (parts.length >= 2) {
    if (parts[1].length == 4) {
      script = parts[1];
      if (parts.length >= 3) region = parts[2];
    } else {
      region = parts[1];
    }
  }
  return _localeFor(language, script: script, region: region);
}

Locale? _localeFor(
  String language, {
  required String script,
  required String region,
}) {
  switch (language) {
    case 'in':
      return const Locale('id');
    case 'tl':
      return const Locale('fil');
    case 'zh':
      return _chinese(script: script, region: region);
    default:
      if (_supported.contains(language)) return Locale(language);
      return null;
  }
}

Locale? _chinese({required String script, required String region}) {
  if (script == 'hant') return null;
  if (script == 'hans') {
    return const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans');
  }
  final country = region.toUpperCase();
  if (country == 'TW' || country == 'HK' || country == 'MO') return null;
  return const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans');
}
