import 'dart:ui';

import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'fallback_delegates.dart';

const kAppLocalePref = 'rs_app_locale';

/// Автоніми, як у перемикачі вітрини. Окремого рядка в таблицях для підпису «Мова» немає.
const appLanguageOptions = <(String code, String label)>[
  ('uk', 'Українська'),
  ('en', 'English'),
  ('zh-hans', '中文'),
  ('ms', 'Bahasa Melayu'),
  ('fil', 'Filipino'),
  ('id', 'Bahasa Indonesia'),
  ('vi', 'Tiếng Việt'),
];

const _deviceLanguages = {'uk', 'en', 'ms', 'fil', 'id', 'vi'};

Locale localeFromCode(String code) {
  switch (code) {
    case 'en':
      return const Locale('en');
    case 'zh':
    case 'zh-hans':
    case 'zh_Hans':
      return const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans');
    case 'ms':
      return const Locale('ms');
    case 'fil':
      return const Locale('fil');
    case 'id':
      return const Locale('id');
    case 'vi':
      return const Locale('vi');
    default:
      return const Locale('uk');
  }
}

String apiLanguageCode(Locale locale) {
  if (locale.languageCode == 'zh') return 'zh-hans';
  return locale.languageCode;
}

Locale matchDeviceLocale(Locale device) {
  final code = device.languageCode.toLowerCase();
  if (code == 'zh') {
    final script = (device.scriptCode ?? '').toLowerCase();
    final country = (device.countryCode ?? '').toUpperCase();
    if (script == 'hant' || country == 'TW' || country == 'HK' || country == 'MO') {
      return const Locale('uk');
    }
    return const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans');
  }
  if (_deviceLanguages.contains(code)) return Locale(code);
  return const Locale('uk');
}

final initialLocaleProvider = Provider<Locale>((ref) => const Locale('uk'));

class AppLocaleController extends Notifier<Locale> {
  @override
  Locale build() => ref.watch(initialLocaleProvider);

  Future<void> select(String code) async {
    final locale = localeFromCode(code);
    state = locale;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(kAppLocalePref, apiLanguageCode(locale));
    } catch (_) {}
  }
}

final appLocaleProvider =
    NotifierProvider<AppLocaleController, Locale>(AppLocaleController.new);

Future<Locale> loadInitialLocale() async {
  try {
    final prefs = await SharedPreferences.getInstance();
    final saved = prefs.getString(kAppLocalePref);
    if (saved != null && saved.isNotEmpty) return localeFromCode(saved);
  } catch (_) {}
  return matchDeviceLocale(PlatformDispatcher.instance.locale);
}

String textOr(String remote, String fallback) => remote.isEmpty ? fallback : remote;

final List<LocalizationsDelegate<dynamic>> appLocalizationDelegates = [
  ...AppLocalizations.localizationsDelegates,
  const FilMaterialFallbackDelegate(),
  const FilCupertinoFallbackDelegate(),
  const FilWidgetsFallbackDelegate(),
];
