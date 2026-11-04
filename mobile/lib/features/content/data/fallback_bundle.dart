import 'package:royal_smoke/features/content/domain/app_content.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

String _paragraphs(List<String> parts) => parts.join('\n\n');

/// Локальний fallback, якщо API / кеш недоступні.
AppContentBundle buildFallbackBundle(AppLocalizations t) {
  return AppContentBundle(
    settings: AppSettingsContent(
      appVersion: t.appVersion,
      appBlurb: t.appBlurb,
      contactAddress: t.contactAddress,
      contactPhone: t.contactPhone,
      contactHours: t.contactHours,
      contactLat: 0,
      contactLng: 0,
    ),
    screens: {
      'splash': AppScreenContent(
        kicker: t.splashKicker,
        title: t.splashTitle,
        ctaPrimary: t.splashOpen,
      ),
      'age': AppScreenContent(
        kicker: t.ageKicker,
        title: t.ageTitle,
        subtitle: t.ageBadge,
        body: t.ageBody,
        legalNote: t.ageLegal,
        confirmLabel: t.ageConfirm,
        ctaSecondary: t.ageExit,
      ),
      'home': AppScreenContent(
        kicker: t.homeKicker,
        title: t.homeTitle,
        body: t.homeBody,
        ctaPrimary: t.bookVisit,
        ctaSecondary: t.houseTab,
        heroAssetFallback: 'assets/images/home/hero.jpg',
      ),
      'house': AppScreenContent(
        kicker: t.houseKicker,
        title: t.houseTitle,
        body: t.houseBody,
        ctaPrimary: t.bookVisit,
        ctaSecondary: t.contacts,
        heroAssetFallback: 'assets/images/home/house.jpg',
        houseBlocks: [
          AppHouseBlock(indexLabel: t.houseBlock1Index, title: t.houseBlockServiceTitle, body: t.houseBlockServiceBody),
          AppHouseBlock(indexLabel: t.houseBlock2Index, title: t.houseBlockB2bTitle, body: t.houseBlockB2bBody),
          AppHouseBlock(indexLabel: t.houseBlock3Index, title: t.visitTitle, body: t.houseBlockVisitBody),
        ],
      ),
      'visit': AppScreenContent(
        kicker: t.visitKicker,
        title: t.visitTitle,
        ctaPrimary: t.visitSendRequest,
        successTitle: t.visitSuccessTitle,
        successBody: t.visitSuccessBody,
        bodySecondary: t.visitNewRequest,
      ),
    },
    pages: {
      'privacy': AppLegalPage(
        slug: 'privacy',
        title: t.privacyTitle,
        body: _paragraphs([t.privacyBody1, t.privacyBody2, t.privacyBody3, t.privacyBody4, t.privacyBody5]),
      ),
      'terms': AppLegalPage(
        slug: 'terms',
        title: t.termsTitle,
        body: _paragraphs([t.termsBody1, t.termsBody2, t.termsBody3, t.termsBody4, t.termsBody5]),
      ),
      'age': AppLegalPage(
        slug: 'age',
        title: t.agePolicyTitle,
        body: _paragraphs([
          t.agePolicyBody1,
          t.agePolicyBody2,
          t.agePolicyBody3,
          t.agePolicyBody4,
          t.agePolicyBody5,
        ]),
      ),
      'about': AppLegalPage(
        slug: 'about',
        title: t.aboutTitle,
        body: _paragraphs([t.aboutBody1, t.aboutBody2, t.aboutBody3, t.aboutBody4, t.aboutBody5]),
      ),
    },
  );
}
