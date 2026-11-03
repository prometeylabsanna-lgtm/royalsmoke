import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

Widget l10nApp({
  required Widget home,
  Locale locale = const Locale('uk'),
}) {
  return ProviderScope(
    overrides: [initialLocaleProvider.overrideWithValue(locale)],
    child: MaterialApp(
      locale: locale,
      theme: AppTheme.dark,
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: appLocalizationDelegates,
      home: home,
    ),
  );
}
