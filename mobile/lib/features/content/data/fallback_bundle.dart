import 'package:royal_smoke/core/constants/app_copy.dart';
import 'package:royal_smoke/features/brands/data/partner_catalog.dart';
import 'package:royal_smoke/features/content/domain/app_content.dart';

/// Локальний fallback, якщо API / кеш недоступні.
AppContentBundle buildFallbackBundle() {
  return AppContentBundle(
    settings: AppSettingsContent(
      appVersion: AppCopy.appVersion,
      appBlurb: AppCopy.appBlurb,
      contactAddress: AppCopy.contactAddress,
      contactPhone: AppCopy.contactPhone,
      contactHours: AppCopy.contactHours,
      contactLat: AppCopy.contactLat,
      contactLng: AppCopy.contactLng,
    ),
    brands: PartnerCatalog.brands,
    screens: {
      'splash': const AppScreenContent(
        kicker: 'ДОВІДНИК БРЕНДУ',
        title: 'ROYAL SMOKE',
        ctaPrimary: 'ВІДКРИТИ',
      ),
      'age': const AppScreenContent(
        kicker: AppCopy.ageKicker,
        title: AppCopy.ageTitle,
        subtitle: AppCopy.ageBadge,
        body: AppCopy.ageBody,
        legalNote: AppCopy.ageLegal,
        confirmLabel: AppCopy.ageConfirm,
        ctaSecondary: 'ВИЙТИ',
      ),
      'home': const AppScreenContent(
        kicker: 'ДІМ БРЕНДУ',
        title: 'ROYAL\nSMOKE',
        body: 'Довідник дому бренду та партнерів',
        ctaPrimary: 'Бренди',
        ctaSecondary: 'Дім',
        heroAssetFallback: 'assets/images/home/hero.jpg',
      ),
      'house': const AppScreenContent(
        kicker: 'Про дім',
        title: 'Дім\nRoyal Smoke',
        body:
            'Royal Smoke — дім, що представляє в Україні родинні бренди з багаторічною історією. '
            'Тут можна дізнатися про походження брендів і познайомитися з колекцією під час візиту.',
        ctaPrimary: 'Забронювати візит',
        ctaSecondary: 'Контакти',
        heroAssetFallback: 'assets/images/home/house.jpg',
        houseBlocks: [
          AppHouseBlock(
            indexLabel: '01',
            title: 'Сервіс',
            body: 'Консультації щодо брендів, історії та зберігання.',
          ),
          AppHouseBlock(
            indexLabel: '02',
            title: 'B2B',
            body: 'Співпраця із закладами та професійними партнерами.',
          ),
          AppHouseBlock(
            indexLabel: '03',
            title: 'Візит',
            body: 'Знайомство з домом за попереднім записом.',
          ),
        ],
      ),
      'visit': const AppScreenContent(
        kicker: 'Дім Royal Smoke',
        title: 'Візит',
        ctaPrimary: 'Надіслати запит',
        successTitle: 'ЗАПИТ НАДІСЛАНО',
        successBody: 'Ми звʼяжемося з вами, щоб підтвердити дату та час візиту.',
        bodySecondary: 'НОВИЙ ЗАПИТ',
      ),
    },
    pages: {
      'privacy': const AppLegalPage(
        slug: 'privacy',
        title: 'Політика конфіденційності',
        body: AppCopy.privacyBody,
      ),
      'terms': const AppLegalPage(slug: 'terms', title: 'Умови', body: AppCopy.termsBody),
      'age': const AppLegalPage(slug: 'age', title: 'Вікова політика', body: AppCopy.agePolicyBody),
      'about': const AppLegalPage(slug: 'about', title: 'Про застосунок', body: AppCopy.aboutBody),
    },
  );
}
