import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/features/booking/presentation/visit_screen.dart';
import 'package:royal_smoke/features/home/presentation/home_screen.dart';

import 'l10n_app.dart';

void main() {
  testWidgets('головна і візит не переповнюються на вузькому екрані', (tester) async {
    tester.view.physicalSize = const Size(320, 568);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(l10nApp(home: const Scaffold(body: HomeScreen())));
    await tester.pump();
    expect(tester.takeException(), isNull);

    await tester.pumpWidget(l10nApp(home: const Scaffold(body: VisitScreen())));
    await tester.pump();
    expect(find.text('ВІЗИТ'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
