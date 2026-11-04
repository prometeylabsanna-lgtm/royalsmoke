import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';
import 'package:royal_smoke/features/booking/presentation/visit_screen.dart';
import 'package:royal_smoke/features/contacts/presentation/contacts_screen.dart';
import 'package:royal_smoke/features/content/data/app_content_repository.dart';
import 'package:royal_smoke/features/content/data/fallback_bundle.dart';
import 'package:royal_smoke/features/content/domain/app_content.dart';
import 'package:royal_smoke/features/content/presentation/app_content_provider.dart';
import 'package:royal_smoke/features/home/presentation/home_screen.dart';
import 'package:royal_smoke/features/house/presentation/house_screen.dart';
import 'package:royal_smoke/features/more/presentation/more_screen.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:royal_smoke/shared/widgets/rs_chrome.dart';

class _FallbackRepository extends AppContentRepository {
  @override
  Future<AppContentBundle> load({
    required String lang,
    required AppLocalizations l10n,
    bool forceNetwork = false,
  }) {
    return Future<AppContentBundle>.value(buildFallbackBundle(l10n));
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  const tops = <double>[59, 47, 24, 30];

  Future<void> pumpScreen(
    WidgetTester tester,
    Widget screen, {
    required double top,
    double bottom = 0,
    double viewTop = -1,
  }) async {
    final resolvedViewTop = viewTop < 0 ? top : viewTop;
    tester.view.devicePixelRatio = 1;
    tester.view.physicalSize = const Size(390, 844);
    tester.view.padding = FakeViewPadding(top: top, bottom: bottom);
    tester.view.viewPadding = FakeViewPadding(
      top: resolvedViewTop,
      bottom: bottom,
    );
    await tester.pumpWidget(_host(screen));
    await tester.pump();
  }

  testWidgets('брівка House, Visit і More нижче за статус-бар', (
    tester,
  ) async {
    addTearDown(tester.view.reset);
    const screens = <(Widget, String)>[
      (HouseScreen(), 'ПРО ДІМ'),
      (VisitScreen(), 'ДІМ ROYAL SMOKE'),
      (MoreScreen(), 'ROYAL SMOKE'),
    ];

    for (final top in tops) {
      final topsY = <double>[];
      for (final entry in screens) {
        await pumpScreen(tester, entry.$1, top: top);
        expect(tester.takeException(), isNull, reason: '${entry.$2} top=$top');
        final dy = tester.getTopLeft(find.text(entry.$2)).dy;
        expect(
          dy,
          greaterThanOrEqualTo(top),
          reason: '${entry.$2} y=$dy top=$top',
        );
        topsY.add(dy);
      }
      final first = topsY.first;
      for (final dy in topsY) {
        expect((dy - first).abs(), lessThan(1), reason: 'top=$top ys=$topsY');
      }
    }
  });

  testWidgets('брівка House читає viewPadding, навіть якщо padding.top = 0', (
    tester,
  ) async {
    addTearDown(tester.view.reset);
    await pumpScreen(tester, const HouseScreen(), top: 0, viewTop: 59);
    final dy = tester.getTopLeft(find.text('ПРО ДІМ')).dy;
    expect(dy, greaterThanOrEqualTo(59));
  });

  testWidgets('Home і контакти: верхній текст нижче за інсет', (
    tester,
  ) async {
    addTearDown(tester.view.reset);
    for (final top in tops) {
      await pumpScreen(tester, const HomeScreen(), top: top);
      expect(tester.takeException(), isNull);
      expect(
        tester.getTopLeft(find.text('ДІМ БРЕНДУ')).dy,
        greaterThanOrEqualTo(top),
        reason: 'home top=$top',
      );

      await pumpScreen(tester, const ContactsScreen(), top: top);
      expect(tester.takeException(), isNull);
      expect(
        tester.getTopLeft(find.text('ЩЕ')).dy,
        greaterThanOrEqualTo(top),
        reason: 'contacts top=$top',
      );
    }
  });

  testWidgets('таб-бар тримає підпис над home indicator і жестом Android', (
    tester,
  ) async {
    addTearDown(tester.view.reset);
    tester.view.devicePixelRatio = 1;
    tester.view.physicalSize = const Size(390, 844);

    Future<void> expectLabelAbove(double inset) async {
      await tester.pumpWidget(
        _host(
          Scaffold(
            body: const SizedBox.expand(),
            bottomNavigationBar: RsTabBar(
              current: RsTab.home,
              onChanged: (_) {},
            ),
          ),
        ),
      );
      await tester.pump();
      expect(tester.takeException(), isNull);
      final bottom = tester.getRect(find.text('Головна')).bottom;
      expect(bottom, lessThanOrEqualTo(844 - inset));
      expect(bottom, greaterThan(844 - inset - 24));
    }

    tester.view.padding = const FakeViewPadding(bottom: 34);
    tester.view.viewPadding = const FakeViewPadding(bottom: 34);
    await expectLabelAbove(34);

    tester.view.padding = const FakeViewPadding(bottom: 48);
    tester.view.viewPadding = const FakeViewPadding(bottom: 48);
    await expectLabelAbove(48);

    tester.view.padding = FakeViewPadding.zero;
    tester.view.viewPadding = FakeViewPadding.zero;
    tester.view.systemGestureInsets = const FakeViewPadding(bottom: 24);
    await expectLabelAbove(24);
  });
}

Widget _host(Widget home) {
  return ProviderScope(
    overrides: [
      initialLocaleProvider.overrideWithValue(const Locale('uk')),
      appContentRepositoryProvider.overrideWithValue(_FallbackRepository()),
    ],
    child: MaterialApp(
      locale: const Locale('uk'),
      theme: AppTheme.dark,
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: appLocalizationDelegates,
      home: home is Scaffold ? home : Scaffold(body: home),
    ),
  );
}
