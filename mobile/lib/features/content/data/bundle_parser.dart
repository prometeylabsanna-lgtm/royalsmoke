import 'package:royal_smoke/features/content/domain/app_content.dart';

String _heroAsset(String key) => switch (key) {
      'house' => 'assets/images/home/house.jpg',
      'home' => 'assets/images/home/hero.jpg',
      _ => '',
    };

/// Поле `brands` у відповіді навмисно не читається: назви, логотипи й історії не показуємо.
AppContentBundle parseAppBundle(Map<String, dynamic> json, {DateTime? updatedAt}) {
  final settingsJson = (json['settings'] as Map?)?.cast<String, dynamic>() ?? {};
  final screensJson = (json['screens'] as Map?)?.cast<String, dynamic>() ?? {};
  final pagesJson = (json['pages'] as Map?)?.cast<String, dynamic>() ?? {};

  final screens = <String, AppScreenContent>{};
  screensJson.forEach((key, value) {
    if (value is! Map) return;
    final m = value.cast<String, dynamic>();
    final blocks = <AppHouseBlock>[];
    for (final b in (m['house_blocks'] as List?) ?? const []) {
      if (b is! Map) continue;
      blocks.add(AppHouseBlock(
        indexLabel: (b['index_label'] ?? '').toString(),
        title: (b['title'] ?? '').toString(),
        body: (b['body'] ?? '').toString(),
      ));
    }
    screens[key] = AppScreenContent(
      kicker: (m['kicker'] ?? '').toString(),
      title: (m['title'] ?? '').toString(),
      subtitle: (m['subtitle'] ?? '').toString(),
      body: (m['body'] ?? '').toString(),
      bodySecondary: (m['body_secondary'] ?? '').toString(),
      ctaPrimary: (m['cta_primary'] ?? '').toString(),
      ctaSecondary: (m['cta_secondary'] ?? '').toString(),
      confirmLabel: (m['confirm_label'] ?? '').toString(),
      legalNote: (m['legal_note'] ?? '').toString(),
      successTitle: (m['success_title'] ?? '').toString(),
      successBody: (m['success_body'] ?? '').toString(),
      heroImageUrl: (m['hero_image'] ?? '').toString(),
      heroAssetFallback: _heroAsset(key),
      houseBlocks: blocks,
    );
  });

  final pages = <String, AppLegalPage>{};
  pagesJson.forEach((key, value) {
    if (value is! Map) return;
    final m = value.cast<String, dynamic>();
    pages[key] = AppLegalPage(
      slug: (m['slug'] ?? key).toString(),
      title: (m['title'] ?? '').toString(),
      body: (m['body'] ?? '').toString(),
    );
  });

  return AppContentBundle(
    settings: AppSettingsContent(
      appVersion: (settingsJson['app_version'] ?? '').toString(),
      appBlurb: (settingsJson['app_blurb'] ?? '').toString(),
      contactAddress: (settingsJson['contact_address'] ?? '').toString(),
      contactPhone: (settingsJson['contact_phone'] ?? '').toString(),
      contactHours: (settingsJson['contact_hours'] ?? '').toString(),
      contactLat: double.tryParse('${settingsJson['contact_lat']}') ?? 50.4501,
      contactLng: double.tryParse('${settingsJson['contact_lng']}') ?? 30.5226,
      appSealUrl: (settingsJson['app_seal'] ?? '').toString(),
    ),
    screens: screens,
    pages: pages,
    updatedAt: updatedAt,
  );
}
