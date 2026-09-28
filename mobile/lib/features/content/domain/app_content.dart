import '../../brands/domain/partner_brand.dart';

class AppSettingsContent {
  const AppSettingsContent({
    required this.appVersion,
    required this.appBlurb,
    required this.contactAddress,
    required this.contactPhone,
    required this.contactHours,
    required this.contactLat,
    required this.contactLng,
    this.appSealUrl = '',
  });

  final String appVersion;
  final String appBlurb;
  final String contactAddress;
  final String contactPhone;
  final String contactHours;
  final double contactLat;
  final double contactLng;
  final String appSealUrl;
}

class AppScreenContent {
  const AppScreenContent({
    this.kicker = '',
    this.title = '',
    this.subtitle = '',
    this.body = '',
    this.bodySecondary = '',
    this.ctaPrimary = '',
    this.ctaSecondary = '',
    this.confirmLabel = '',
    this.legalNote = '',
    this.successTitle = '',
    this.successBody = '',
    this.heroImageUrl = '',
    this.heroAssetFallback = '',
    this.houseBlocks = const [],
  });

  final String kicker;
  final String title;
  final String subtitle;
  final String body;
  final String bodySecondary;
  final String ctaPrimary;
  final String ctaSecondary;
  final String confirmLabel;
  final String legalNote;
  final String successTitle;
  final String successBody;
  final String heroImageUrl;
  final String heroAssetFallback;
  final List<AppHouseBlock> houseBlocks;
}

class AppHouseBlock {
  const AppHouseBlock({
    required this.indexLabel,
    required this.title,
    required this.body,
  });

  final String indexLabel;
  final String title;
  final String body;
}

class AppLegalPage {
  const AppLegalPage({required this.slug, required this.title, required this.body});

  final String slug;
  final String title;
  final String body;
}

class AppContentBundle {
  const AppContentBundle({
    required this.settings,
    required this.brands,
    required this.screens,
    required this.pages,
    this.updatedAt,
  });

  final AppSettingsContent settings;
  final List<PartnerBrand> brands;
  final Map<String, AppScreenContent> screens;
  final Map<String, AppLegalPage> pages;
  final DateTime? updatedAt;

  PartnerBrand? brandById(String id) {
    for (final b in brands) {
      if (b.id == id) return b;
    }
    return null;
  }

  AppScreenContent screen(String key) =>
      screens[key] ?? const AppScreenContent();

  AppLegalPage? page(String slug) => pages[slug];
}
