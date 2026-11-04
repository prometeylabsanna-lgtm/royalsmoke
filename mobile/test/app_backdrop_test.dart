import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/app.dart';
import 'package:royal_smoke/core/constants/app_images.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/core/theme/app_colors.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';
import 'package:royal_smoke/features/home/presentation/home_screen.dart';
import 'package:royal_smoke/features/house/presentation/house_screen.dart';
import 'package:royal_smoke/shared/widgets/app_backdrop.dart';
import 'package:royal_smoke/shared/widgets/backdrop_motion.dart';
import 'package:royal_smoke/shared/widgets/rs_chrome.dart';
import 'package:royal_smoke/shared/widgets/rs_cover_image.dart';

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

  test('полотно теми рівно #1E1009, app bar прозорий', () {
    final theme = AppTheme.dark;
    expect(theme.scaffoldBackgroundColor, const Color(0xFF1E1009));
    expect(theme.canvasColor, const Color(0xFF1E1009));
    expect(theme.colorScheme.surface, AppColors.canvas);
    expect(theme.appBarTheme.backgroundColor, Colors.transparent);
    expect(AppTheme.overlay.systemNavigationBarColor, AppColors.canvas);
    expect(AppTheme.overlay.statusBarColor, Colors.transparent);
  });

  test('ken-burns тримає ширину і масштаб 2–4%', () {
    expect(BackdropMotion.kenBurnsDuration, const Duration(seconds: 24));
    expect(BackdropMotion.glowDuration, const Duration(seconds: 8));
    expect(BackdropMotion.glowPeakOpacity, 0.15);

    for (final width in const [320.0, 390.0, 440.0, 768.0, 1024.0]) {
      final imageHeight = width * BackdropMotion.imageAspect;
      for (var step = 0; step <= 20; step++) {
        final frame = BackdropMotion.at(
          t: step / 20,
          width: width,
          imageHeight: imageHeight,
        );
        expect(frame.scale, inInclusiveRange(1.02, 1.04));
        final slack = width * (frame.scale - 1) / 2;
        expect(frame.dx.abs(), lessThanOrEqualTo(slack + 0.001));
        expect(frame.dy, lessThanOrEqualTo(0));
        expect(frame.dy, greaterThanOrEqualTo(-imageHeight * 0.02 - 0.001));
      }
    }
  });

  testWidgets('головна і сервіс без окремих hero-карток', (tester) async {
    await tester.pumpWidget(l10nApp(home: const Scaffold(body: HomeScreen())));
    await tester.pump();
    expect(find.byType(RsCoverImage), findsNothing);
    expect(find.text('ПЕРСОНАЛЬНИЙ СЕРВІС'), findsWidgets);
    expect(tester.takeException(), isNull);

    await tester.pumpWidget(l10nApp(home: const Scaffold(body: HouseScreen())));
    await tester.pump();
    expect(find.byType(RsCoverImage), findsNothing);
    expect(find.text('ПРО СЕРВІС'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('спільний фон один і не скидається між маршрутами', (
    tester,
  ) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          initialLocaleProvider.overrideWithValue(const Locale('uk')),
        ],
        child: const RoyalSmokeApp(),
      ),
    );
    await tester.pump();

    expect(find.byType(AppBackdrop), findsOneWidget);
    expect(_backgroundImages, findsOneWidget);
    final backdrop = tester.state<AppBackdropState>(find.byType(AppBackdrop));
    expect(backdrop.motionRunning, isFalse);
    expect(backdrop.kenBurnsT, 0);

    await tester.pump(const Duration(milliseconds: 400));
    expect(backdrop.kenBurnsT, 0);
    expect(backdrop.motionRunning, isFalse);

    await tester.tap(find.text('ВІДКРИТИ'));
    await tester.pumpAndSettle();
    expect(find.text('ВІКОВЕ ОБМЕЖЕННЯ 21+'), findsOneWidget);
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );
    expect(_backgroundImages, findsOneWidget);

    final scaffold = tester.widget<Scaffold>(find.byType(Scaffold));
    expect(scaffold.backgroundColor, Colors.transparent);

    await tester.tap(find.text('МЕНІ Є 21 РІК'));
    await tester.pumpAndSettle();
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );
    expect(_backgroundImages, findsOneWidget);
    expect(find.byType(RsCoverImage), findsNothing);

    final bars = tester.widgetList<DecoratedBox>(
      find.descendant(
        of: find.byType(RsTabBar),
        matching: find.byType(DecoratedBox),
      ),
    );
    expect(
      bars.any((box) {
        final decoration = box.decoration;
        return decoration is BoxDecoration &&
            decoration.color == AppColors.canvas;
      }),
      isTrue,
    );

    await tester.tap(find.text('Сервіс'));
    await tester.pumpAndSettle();
    expect(find.text('ПРО СЕРВІС'), findsOneWidget);
    expect(find.byType(RsCoverImage), findsNothing);
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );
    expect(_backgroundImages, findsOneWidget);
  });

  testWidgets('анімація йде і не перезапускається на вкладці', (tester) async {
    TestWidgetsFlutterBinding
        .instance
        .platformDispatcher
        .accessibilityFeaturesTestValue = const FakeAccessibilityFeatures(
      disableAnimations: false,
    );

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          initialLocaleProvider.overrideWithValue(const Locale('uk')),
        ],
        child: const RoyalSmokeApp(),
      ),
    );
    await tester.pump();
    final backdrop = tester.state<AppBackdropState>(find.byType(AppBackdrop));
    expect(backdrop.motionRunning, isTrue);

    await tester.tap(find.text('ВІДКРИТИ'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(find.text('ВІКОВЕ ОБМЕЖЕННЯ 21+'), findsOneWidget);
    await tester.tap(find.text('МЕНІ Є 21 РІК'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(find.text('ЗАЛИШИТИ ЗАПИТ'), findsOneWidget);
    await tester.pump(const Duration(seconds: 3));

    final before = backdrop.kenBurnsT;
    expect(before, greaterThan(0.05));
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );

    await tester.tap(find.text('Сервіс'));
    await tester.pump(const Duration(milliseconds: 400));
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );
    expect(backdrop.kenBurnsT, greaterThan(before));
    expect(backdrop.motionRunning, isTrue);

    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pump();
  });
}

final Finder _backgroundImages = find.byWidgetPredicate((widget) {
  if (widget is! Image) return false;
  final provider = widget.image;
  return provider is AssetImage &&
      provider.assetName == AppImages.appBackground;
});
