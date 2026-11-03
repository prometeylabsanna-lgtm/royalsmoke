import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/core/router/app_router.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

class RoyalSmokeApp extends ConsumerStatefulWidget {
  const RoyalSmokeApp({super.key});

  @override
  ConsumerState<RoyalSmokeApp> createState() => _RoyalSmokeAppState();
}

class _RoyalSmokeAppState extends ConsumerState<RoyalSmokeApp> {
  late final _router = buildAppRouter();

  @override
  Widget build(BuildContext context) {
    final locale = ref.watch(appLocaleProvider);
    return MaterialApp.router(
      title: lookupAppLocalizations(locale).appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.dark,
      locale: locale,
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: appLocalizationDelegates,
      routerConfig: _router,
    );
  }
}
