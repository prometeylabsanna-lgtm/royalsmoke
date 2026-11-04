import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/app.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/features/more/presentation/more_screen.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:royal_smoke/shared/widgets/rs_chrome.dart';

import 'l10n_app.dart';

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
    expect(uk.tabHome, 'Головна');
    expect(en.tabHome, 'Home');
    for (final locale in AppLocalizations.supportedLocales) {
      expect(
        lookupAppLocalizations(locale).tabHome.trim(),
        isNotEmpty,
        reason: locale.toLanguageTag(),
      );
    }
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
    await _pumpRoute(tester);
    expect(find.text('ВІКОВЕ ОБМЕЖЕННЯ 21+'), findsOneWidget);

    await tester.tap(find.text('МЕНІ Є 21 РІК'));
    await _pumpRoute(tester);
    expect(
      find.text(
        'Залиште запит у застосунку — менеджер звʼяжеться з вами у зручний спосіб.',
      ),
      findsOneWidget,
    );
    expect(find.text('ПЕРСОНАЛЬНИЙ СЕРВІС'), findsWidgets);
    expect(find.text('ЗАЛИШИТИ ЗАПИТ'), findsOneWidget);
    expect(find.byIcon(Icons.home), findsOneWidget);
    expect(find.byIcon(Icons.room_service_outlined), findsOneWidget);
    final tabLabels = ['Головна', 'Сервіс', 'Запит', 'Контакти', 'Ще'];
    double? tabLeft;
    for (final label in tabLabels) {
      final rect = tester.getRect(
        find.descendant(of: find.byType(RsTabBar), matching: find.text(label)),
      );
      if (tabLeft != null) {
        expect(rect.left, greaterThan(tabLeft), reason: label);
      }
      tabLeft = rect.left;
    }
    expect(find.text('Сервіс'), findsOneWidget);
    expect(find.text('Контакти'), findsWidgets);
    expect(find.text('Ще'), findsOneWidget);
    expect(find.text('Бренди'), findsNothing);

    await tester.tap(find.text('Запит'));
    await _pumpRoute(tester);
    expect(find.text('ЗАПИТ'), findsOneWidget);
    expect(find.text('ЗРУЧНИЙ ЧАС ДЛЯ ЗВʼЯЗКУ'), findsOneWidget);
    expect(find.textContaining('Купити'), findsNothing);
    await _releaseApp(tester);
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
    await _pumpRoute(tester);
    expect(find.text('AGE RESTRICTION 21+'), findsOneWidget);
    expect(find.text('I AM 21 OR OLDER'), findsOneWidget);
    await _releaseApp(tester);
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
    await _releaseApp(tester);
  });

  testWidgets('заголовок ЩЕ без широкого трекінгу', (tester) async {
    await tester.pumpWidget(l10nApp(home: const Scaffold(body: MoreScreen())));
    await tester.pump();
    final title = tester.widget<Text>(find.text('ЩЕ'));
    expect(title.style?.letterSpacing, lessThanOrEqualTo(28 * 0.04));
    expect(tester.takeException(), isNull);
  });
}

Future<void> _pumpRoute(WidgetTester tester) async {
  await tester.pump();
  await tester.pump(const Duration(milliseconds: 400));
}

Future<void> _releaseApp(WidgetTester tester) async {
  await tester.pumpWidget(const SizedBox.shrink());
  await tester.pump();
}
