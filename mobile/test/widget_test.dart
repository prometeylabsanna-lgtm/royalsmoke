import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/app.dart';

void main() {
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

    await tester.tap(find.text('Бренди'));
    await tester.pumpAndSettle();
    expect(find.text('Casa Turrent'), findsOneWidget);
    expect(find.textContaining('Купити'), findsNothing);
  });
}
