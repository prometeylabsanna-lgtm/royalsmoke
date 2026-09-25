import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';
import 'package:royal_smoke/features/brands/presentation/brand_detail_screen.dart';
import 'package:royal_smoke/features/home/presentation/home_screen.dart';

void main() {
  testWidgets('головна і картка бренду не переповнюються на вузькому екрані', (tester) async {
    tester.view.physicalSize = const Size(320, 568);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      MaterialApp(theme: AppTheme.dark, home: const Scaffold(body: HomeScreen())),
    );
    await tester.pump();
    expect(tester.takeException(), isNull);

    await tester.pumpWidget(
      MaterialApp(
        theme: AppTheme.dark,
        home: const Scaffold(body: BrandDetailScreen(brandId: 'turrent')),
      ),
    );
    await tester.pump();
    expect(find.text('CASA TURRENT'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
