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

  test('parser читає екрани і пропускає brands', () {
    final bundle = parseAppBundle({
      'settings': {
        'app_version': 'v-test',
        'app_blurb': 'blurb',
        'contact_address': 'Київ',
        'contact_phone': '+380',
        'contact_hours': '11-22',
        'contact_lat': 50.45,
        'contact_lng': 30.52,
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
    expect(bundle.screen('home').title, 'T');
    expect(bundle.screen('home').heroImageUrl, isEmpty);
    expect(bundle.page('about')?.title, 'Про');
  });
}
