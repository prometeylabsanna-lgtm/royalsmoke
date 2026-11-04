import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/features/content/data/bundle_parser.dart';
import 'package:royal_smoke/features/content/data/fallback_bundle.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

void main() {
  test('fallback bundle має екрани та політику', () {
    final bundle = buildFallbackBundle(lookupAppLocalizations(const Locale('uk')));
    expect(bundle.screen('home').title, isNotEmpty);
    expect(bundle.screen('visit').ctaPrimary, isNotEmpty);
    expect(bundle.page('privacy')?.body, isNotEmpty);
  });

  test('parser читає екрани і пропускає каталог', () {
    final bundle = parseAppBundle({
      'settings': {
        'app_version': 'v-test',
        'app_blurb': 'blurb',
        'contact_address': '',
        'contact_phone': '+380',
        'contact_hours': '11-22',
        'contact_lat': 0,
        'contact_lng': 0,
        'app_seal': '',
      },
      'brands': [
        {
          'id': 'hidden',
          'name': 'Hidden',
        },
      ],
      'screens': {
        'home': {
          'kicker': 'К',
          'title': 'T',
          'body': 'B',
          'hero_image': '',
          'house_blocks': [],
        },
      },
      'pages': {
        'about': {'slug': 'about', 'title': 'Про', 'body': 'Текст'},
      },
    });

    expect(bundle.settings.appVersion, 'v-test');
    expect(bundle.settings.contactAddress, isEmpty);
    expect(bundle.settings.contactPhone, '+380');
    expect(bundle.settings.contactHours, '11-22');
    expect(bundle.screen('home').title, 'T');
    expect(bundle.screen('home').heroImageUrl, isEmpty);
    expect(bundle.page('about')?.title, 'Про');
  });
}
