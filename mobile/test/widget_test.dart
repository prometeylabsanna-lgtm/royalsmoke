import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/app.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

void main() {
  test('uk та en рядки з таблиць', () {
    final uk = lookupAppLocalizations(const Locale('uk'));
    final en = lookupAppLocalizations(const Locale('en'));
    expect(uk.termsBody2, contains('допомагають'));
    expect(uk.termsBody2.contains('допомогають'), isFalse);
    expect(uk.factFamilyTurrent, 'Туррент');
    expect(en.factFamilyTurrent, 'Turrent');
    expect(uk.appBlurb, contains('дому бренду'));
    expect(en.appBlurb, contains('brand house'));
    expect(uk.aboutBody3, contains('він розповідає'));
    expect(en.aboutBody3, contains('covers the culture'));
    expect(uk.offlineUpdated('01.01.2026'), 'Оновлено 01.01.2026');
    expect(en.offlineUpdated('01.01.2026'), 'Updated 01.01.2026');
  });

  testWidgets('застосунок стартує з темною темою', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: RoyalSmokeApp()));
    expect(find.text('ROYAL SMOKE'), findsOneWidget);
    expect(find.text('21+'), findsOneWidget);

    await tester.tap(find.text('ВІДКРИТИ'));
    await tester.pumpAndSettle();
    expect(find.text('ЛИШЕ ДЛЯ ПОВНОЛІТНІХ'), findsOneWidget);

    await tester.tap(find.text('МЕНІ Є 21 РІК'));
    await tester.pumpAndSettle();
    expect(find.text('Довідник дому бренду та партнерів'), findsOneWidget);

    await tester.tap(find.text('Бренди').last);
    await tester.pumpAndSettle();
    // Назви на картках у uppercase по словах (RsBrandTitle).
    expect(find.text('TURRENT'), findsOneWidget);
    expect(find.textContaining('Купити'), findsNothing);
  });

  testWidgets('англійські рядки рендеряться', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [initialLocaleProvider.overrideWithValue(const Locale('en'))],
        child: const RoyalSmokeApp(),
      ),
    );
    await tester.pump();
    expect(find.text('OPEN'), findsOneWidget);
    expect(find.text('BRAND GUIDE'), findsOneWidget);

    await tester.tap(find.text('OPEN'));
    await tester.pumpAndSettle();
    expect(find.text('ADULTS ONLY'), findsOneWidget);
    expect(find.text('I AM 21+'), findsOneWidget);
  });

  testWidgets('fil не валить Material і Cupertino', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [initialLocaleProvider.overrideWithValue(const Locale('fil'))],
        child: const RoyalSmokeApp(),
      ),
    );
    await tester.pump();
    expect(tester.takeException(), isNull);
    expect(find.text('BUKSAN'), findsOneWidget);
  });
}
