import 'dart:ui';

import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'fallback_delegates.dart';
import 'locale_resolution.dart';

export 'locale_resolution.dart';

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

String apiLanguageCode(Locale locale) {
  if (locale.languageCode == 'zh') return 'zh-hans';
  return locale.languageCode;
}

final initialLocaleProvider = Provider<Locale>((ref) => fallbackLocale);

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

final appLocaleProvider = NotifierProvider<AppLocaleController, Locale>(
  AppLocaleController.new,
);

Future<Locale> loadInitialLocale() async {
  String? saved;
  try {
    final prefs = await SharedPreferences.getInstance();
    saved = prefs.getString(kAppLocalePref);
  } catch (_) {}
  return resolveAppLocale(
    savedCode: saved,
    deviceLocale: PlatformDispatcher.instance.locale,
  );
}

String textOr(String remote, String fallback) =>
    remote.isEmpty ? fallback : remote;

final List<LocalizationsDelegate<dynamic>> appLocalizationDelegates = [
  ...AppLocalizations.localizationsDelegates,
  const FilMaterialFallbackDelegate(),
  const FilCupertinoFallbackDelegate(),
  const FilWidgetsFallbackDelegate(),
];
