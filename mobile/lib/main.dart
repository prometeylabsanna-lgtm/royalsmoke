import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app.dart';
import 'core/l10n/app_locale.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final locale = await loadInitialLocale();
  runApp(
    ProviderScope(
      overrides: [initialLocaleProvider.overrideWithValue(locale)],
      child: const RoyalSmokeApp(),
    ),
  );
}
