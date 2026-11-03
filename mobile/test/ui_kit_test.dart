import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/features/brands/data/partner_catalog.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:royal_smoke/shared/widgets/rs_brand.dart';
import 'package:royal_smoke/shared/widgets/rs_button.dart';
import 'package:royal_smoke/shared/widgets/rs_chrome.dart';

import 'l10n_app.dart';

void main() {
  testWidgets('кіт показує 21+ і Casa Turrent без ціни', (tester) async {
    final l10n = lookupAppLocalizations(const Locale('uk'));
    final turrent = PartnerCatalog.of(l10n).last;
    expect(turrent.name, 'Casa Turrent');
    expect(turrent.country, 'Мексика');

    await tester.pumpWidget(
      l10nApp(
        home: Scaffold(
          body: Column(
            children: [
              const RsAgeBadge(),
              RsButton(label: 'Бренди', onPressed: () {}),
              SizedBox(
                width: 160,
                height: 220,
                child: RsBrandCell(brand: turrent),
              ),
            ],
          ),
        ),
      ),
    );

    expect(find.text('21+'), findsOneWidget);
    expect(find.text('БРЕНДИ'), findsOneWidget);
    expect(find.text('CASA'), findsOneWidget);
    expect(find.text('TURRENT'), findsOneWidget);
    expect(find.textContaining('₴'), findsNothing);
    expect(find.textContaining('Купити'), findsNothing);
  });
}
