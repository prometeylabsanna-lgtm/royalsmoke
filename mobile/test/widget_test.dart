import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/app.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

void main() {
  setUp(() {
    TestWidgetsFlutterBinding
        .instance
        .platformDispatcher
        .accessibilityFeaturesTestValue = const FakeAccessibilityFeatures(
      disableAnimations: true,
    );
  });

  test('uk та en рядки з таблиць', () {
    final uk = lookupAppLocalizations(const Locale('uk'));
    final en = lookupAppLocalizations(const Locale('en'));
    expect(uk.termsBody2, contains('запит'));
    expect(uk.termsBody2.toLowerCase().contains('лаунж'), isFalse);
    expect(uk.houseTab, 'Сервіс');
    expect(en.houseTab, 'Service');
    expect(uk.contactAddress, isEmpty);
    expect(en.contactAddress, isEmpty);
    expect(uk.appBlurb.toLowerCase(), contains('персональний сервіс'));
    expect(en.appBlurb.toLowerCase(), contains('personal service'));
    expect(uk.aboutBody1.toLowerCase(), contains('персонального сервісу'));
    expect(en.aboutBody1.toLowerCase(), contains('personal service'));
    expect(uk.visitTitle, 'Запит');
    expect(en.visitTitle, 'Request');
    expect(uk.dateLabel, 'Зручний час для звʼязку');
    expect(en.dateLabel, 'Convenient time to get in touch');
    expect(uk.appName, 'RoyalSmoke');
    expect(en.appName, 'RoyalSmoke');
  });

  testWidgets('застосунок стартує з темною темою', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          initialLocaleProvider.overrideWithValue(const Locale('uk')),
        ],
        child: const RoyalSmokeApp(),
      ),
    );
    expect(find.text('ROYALSMOKE'), findsOneWidget);
    expect(find.text('21+'), findsOneWidget);

    await tester.tap(find.text('ВІДКРИТИ'));
    await tester.pumpAndSettle();
    expect(find.text('ВІКОВЕ ОБМЕЖЕННЯ 21+'), findsOneWidget);

    await tester.tap(find.text('МЕНІ Є 21 РІК'));
    await tester.pumpAndSettle();
    expect(
      find.text(
        'Залиште запит у застосунку — менеджер звʼяжеться з вами у зручний спосіб.',
      ),
      findsOneWidget,
    );
    expect(find.text('ПЕРСОНАЛЬНИЙ СЕРВІС'), findsWidgets);
    expect(find.text('ЗАЛИШИТИ ЗАПИТ'), findsOneWidget);
    expect(find.text('Головна'), findsNothing);
    expect(find.text('Сервіс'), findsOneWidget);
    expect(find.text('Контакти'), findsWidgets);
    expect(find.text('Ще'), findsOneWidget);
    expect(find.text('Бренди'), findsNothing);

    await tester.tap(find.text('Запит'));
    await tester.pumpAndSettle();
    expect(find.text('ЗАПИТ'), findsOneWidget);
    expect(find.text('ЗРУЧНИЙ ЧАС ДЛЯ ЗВʼЯЗКУ'), findsOneWidget);
    expect(find.textContaining('Купити'), findsNothing);
  });

  testWidgets('англійські рядки рендеряться', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          initialLocaleProvider.overrideWithValue(const Locale('en')),
        ],
        child: const RoyalSmokeApp(),
      ),
    );
    await tester.pump();
    expect(find.text('OPEN'), findsOneWidget);
    expect(find.text('PERSONAL SERVICE'), findsOneWidget);

    await tester.tap(find.text('OPEN'));
    await tester.pumpAndSettle();
    expect(find.text('AGE RESTRICTION 21+'), findsOneWidget);
    expect(find.text('I AM 21 OR OLDER'), findsOneWidget);
  });

  testWidgets('fil не валить Material і Cupertino', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          initialLocaleProvider.overrideWithValue(const Locale('fil')),
        ],
        child: const RoyalSmokeApp(),
      ),
    );
    await tester.pump();
    expect(tester.takeException(), isNull);
    expect(find.text('BUKSAN'), findsOneWidget);
  });
}
