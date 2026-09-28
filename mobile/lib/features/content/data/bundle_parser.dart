import 'package:royal_smoke/features/brands/domain/partner_brand.dart';
import 'package:royal_smoke/features/content/domain/app_content.dart';

BrandPanel _panel(String raw) => switch (raw) {
      'burgundy' => BrandPanel.burgundy,
      'green' => BrandPanel.green,
      'brown' => BrandPanel.brown,
      _ => BrandPanel.amber,
    };

String _assetForSlug(String slug) => switch (slug) {
      'aj' => 'assets/images/brands/aj.jpg',
      'oliva' => 'assets/images/brands/oliva.jpg',
      'perdomo' => 'assets/images/brands/perdomo.jpg',
      'turrent' => 'assets/images/brands/turrent.jpg',
      _ => 'assets/images/brands/aj.jpg',
    };

String _heroAsset(String key) => switch (key) {
      'house' => 'assets/images/home/house.jpg',
      'home' => 'assets/images/home/hero.jpg',
      _ => '',
    };

AppContentBundle parseAppBundle(Map<String, dynamic> json, {DateTime? updatedAt}) {
  final settingsJson = (json['settings'] as Map?)?.cast<String, dynamic>() ?? {};
  final brandsJson = (json['brands'] as List?) ?? const [];
  final screensJson = (json['screens'] as Map?)?.cast<String, dynamic>() ?? {};
  final pagesJson = (json['pages'] as Map?)?.cast<String, dynamic>() ?? {};

  final brands = <PartnerBrand>[];
  for (final raw in brandsJson) {
    if (raw is! Map) continue;
    final m = raw.cast<String, dynamic>();
    final id = (m['id'] ?? m['slug'] ?? '').toString();
    if (id.isEmpty) continue;
    final facts = <BrandFact>[];
    for (final f in (m['facts'] as List?) ?? const []) {
      if (f is! Map) continue;
      facts.add(BrandFact(
        label: (f['label'] ?? '').toString(),
        value: (f['value'] ?? '').toString(),
      ));
    }
    final lines = <String>[];
    for (final l in (m['lines'] as List?) ?? const []) {
      if (l is String) {
        lines.add(l);
      } else if (l is Map && l['name'] != null) {
        lines.add(l['name'].toString());
      }
    }
    final photos = <String>[];
    for (final p in (m['photos'] as List?) ?? const []) {
      if (p is Map && (p['image'] ?? '').toString().isNotEmpty) {
        photos.add(p['image'].toString());
      }
    }
    brands.add(PartnerBrand(
      id: id,
      mono: (m['mono'] ?? '').toString(),
      shortName: (m['short_name'] ?? m['name'] ?? '').toString(),
      name: (m['name'] ?? '').toString(),
      country: (m['country'] ?? '').toString(),
      panel: _panel((m['panel'] ?? 'amber').toString()),
      imageAsset: _assetForSlug(id),
      imageUrl: (m['cover'] ?? '').toString(),
      photoUrls: photos,
      heritage: (m['heritage'] ?? '').toString(),
      facts: facts,
      lines: lines,
    ));
  }

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
    brands: brands,
    screens: screens,
    pages: pages,
    updatedAt: updatedAt,
  );
}
