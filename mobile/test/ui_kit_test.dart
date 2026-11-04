import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/shared/widgets/rs_button.dart';
import 'package:royal_smoke/shared/widgets/rs_chrome.dart';

import 'l10n_app.dart';

void main() {
  testWidgets('кіт показує 21+ без ціни', (tester) async {
    await tester.pumpWidget(
      l10nApp(
        home: Scaffold(
          body: Column(
            children: [
              const RsAgeBadge(),
              RsButton(label: 'Контакти', onPressed: () {}),
            ],
          ),
        ),
      ),
    );

    expect(find.text('21+'), findsOneWidget);
    expect(find.text('КОНТАКТИ'), findsOneWidget);
    expect(find.textContaining('₴'), findsNothing);
    expect(find.textContaining('Купити'), findsNothing);
  });
}
