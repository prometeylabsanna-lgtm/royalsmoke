import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';
import 'package:royal_smoke/features/brands/data/partner_catalog.dart';
import 'package:royal_smoke/shared/widgets/rs_brand.dart';
import 'package:royal_smoke/shared/widgets/rs_button.dart';
import 'package:royal_smoke/shared/widgets/rs_chrome.dart';

void main() {
  testWidgets('кіт показує 21+ і Casa Turrent без ціни', (tester) async {
    final turrent = PartnerCatalog.brands.last;
    expect(turrent.name, 'Casa Turrent');
    expect(turrent.country, 'Мексика');

    await tester.pumpWidget(
      MaterialApp(
        theme: AppTheme.dark,
        home: Scaffold(
          body: Column(
            children: [
              const RsAgeBadge(),
              RsButton(label: 'Бренди', onPressed: () {}),
              SizedBox(width: 160, child: RsBrandCell(brand: turrent)),
            ],
          ),
        ),
      ),
    );

    expect(find.text('21+'), findsOneWidget);
    expect(find.text('БРЕНДИ'), findsOneWidget);
    expect(find.text('Casa Turrent'), findsOneWidget);
    expect(find.textContaining('₴'), findsNothing);
    expect(find.textContaining('Купити'), findsNothing);
  });
}
