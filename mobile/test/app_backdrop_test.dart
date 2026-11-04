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

  test('полотно теми рівно #1B1715, app bar прозорий', () {
    final theme = AppTheme.dark;
    expect(theme.scaffoldBackgroundColor, const Color(0xFF1B1715));
    expect(theme.canvasColor, const Color(0xFF1B1715));
    expect(theme.colorScheme.surface, AppColors.canvas);
    expect(AppColors.canvasClear, const Color(0x001B1715));
    expect(AppColors.backdropDim, const Color(0x991B1715));
    expect(theme.appBarTheme.backgroundColor, Colors.transparent);
    expect(AppTheme.overlay.systemNavigationBarColor, AppColors.canvas);
    expect(AppTheme.overlay.statusBarColor, Colors.transparent);
  });

  test('ken-burns 6 с, краї кадру лишаються закриті', () {
    expect(BackdropMotion.kenBurnsDuration, const Duration(seconds: 6));
    expect(BackdropMotion.glowDuration, const Duration(seconds: 6));
    expect(BackdropMotion.glowPeakOpacity, 0.35);

    const bleed = 2.0;
    for (final width in const [320.0, 390.0, 440.0, 768.0, 1024.0]) {
      final plateWidth = width + bleed * 2;
      final imageHeight = plateWidth * BackdropMotion.imageAspect;
      for (var step = 0; step <= 20; step++) {
        final t = step / 20;
        final frame = BackdropMotion.at(
          t: t,
          width: width,
          imageHeight: imageHeight,
        );
        expect(frame.scale, closeTo(1.0 + 0.12 * t, 0.0001));
        final slack = width * (frame.scale - 1) / 2;
        expect(frame.dx, closeTo(slack * 0.6 * (2 * t - 1), 0.001));
        expect(frame.dx.abs(), lessThanOrEqualTo(slack + 0.001));
        expect(frame.dy, closeTo(-imageHeight * 0.03 * t, 0.001));
        expect(frame.dy, lessThanOrEqualTo(0));

        final left = width / 2 - plateWidth * frame.scale / 2 + frame.dx;
        final right = width / 2 + plateWidth * frame.scale / 2 + frame.dx;
        expect(left, lessThanOrEqualTo(0.001));
        expect(right, greaterThanOrEqualTo(width - 0.001));
        expect(
          imageHeight * frame.scale + frame.dy,
          greaterThanOrEqualTo(imageHeight - 0.001),
        );
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
    expect(find.byType(ColorFiltered), findsOneWidget);
    expect(_backgroundImages, findsOneWidget);
    final backdrop = tester.state<AppBackdropState>(find.byType(AppBackdrop));
    expect(backdrop.motionRunning, isTrue);

    final started = backdrop.kenBurnsT;
    await tester.pump(const Duration(milliseconds: 400));
    expect(backdrop.kenBurnsT, greaterThan(started));
    expect(backdrop.motionRunning, isTrue);

    await tester.tap(find.text('ВІДКРИТИ'));
    await _pumpRoute(tester);
    expect(find.text('ВІКОВЕ ОБМЕЖЕННЯ 21+'), findsOneWidget);
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );
    expect(_backgroundImages, findsOneWidget);

    final scaffold = tester.widget<Scaffold>(find.byType(Scaffold));
    expect(scaffold.backgroundColor, Colors.transparent);

    await tester.tap(find.text('МЕНІ Є 21 РІК'));
    await _pumpRoute(tester);
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
    await _pumpRoute(tester);
    expect(find.text('ПРО СЕРВІС'), findsOneWidget);
    expect(find.byType(RsCoverImage), findsNothing);
    expect(
      tester.state<AppBackdropState>(find.byType(AppBackdrop)),
      same(backdrop),
    );
    expect(_backgroundImages, findsOneWidget);
    await _releaseApp(tester);
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

Future<void> _pumpRoute(WidgetTester tester) async {
  await tester.pump();
  await tester.pump(const Duration(milliseconds: 400));
}

Future<void> _releaseApp(WidgetTester tester) async {
  await tester.pumpWidget(const SizedBox.shrink());
  await tester.pump();
}

final Finder _backgroundImages = find.byWidgetPredicate((widget) {
  if (widget is! Image) return false;
  final provider = widget.image;
  return provider is AssetImage &&
      provider.assetName == AppImages.appBackground;
});
