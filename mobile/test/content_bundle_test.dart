import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/features/content/data/bundle_parser.dart';
import 'package:royal_smoke/features/content/data/fallback_bundle.dart';

void main() {
  test('fallback bundle має бренди та екрани', () {
    final bundle = buildFallbackBundle();
    expect(bundle.brands.length, greaterThanOrEqualTo(4));
    expect(bundle.screen('home').title, isNotEmpty);
    expect(bundle.page('privacy')?.body, isNotEmpty);
  });

  test('parser читає bundle JSON', () {
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
          'id': 'aj',
          'slug': 'aj',
          'name': 'AJ Fernandez',
          'short_name': 'AJ',
          'mono': 'AJ',
          'country': 'Нікарагуа',
          'panel': 'amber',
          'cover': 'https://example.com/aj.jpg',
          'heritage': 'story',
          'facts': [
            {'label': 'A', 'value': 'B'},
          ],
          'lines': ['Line 1'],
          'photos': [],
        },
      ],
      'screens': {
        'home': {
          'kicker': 'К',
          'title': 'T',
          'body': 'B',
          'hero_image': 'https://example.com/h.jpg',
          'house_blocks': [],
        },
      },
      'pages': {
        'about': {'slug': 'about', 'title': 'Про', 'body': 'Текст'},
      },
    });

    expect(bundle.settings.appVersion, 'v-test');
    expect(bundle.brands.single.id, 'aj');
    expect(bundle.brands.single.imageUrl, contains('aj.jpg'));
    expect(bundle.screen('home').title, 'T');
    expect(bundle.page('about')?.title, 'Про');
  });
}
