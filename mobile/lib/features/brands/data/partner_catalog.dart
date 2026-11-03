import 'package:royal_smoke/l10n/app_localizations.dart';

import '../domain/partner_brand.dart';

/// Запасний каталог, якщо API недоступне. Тексти залежать від локалі.
abstract final class PartnerCatalog {
  static List<PartnerBrand> of(AppLocalizations t) {
    return [
      PartnerBrand(
        id: 'aj',
        mono: t.brandAjShort,
        shortName: t.brandAjShort,
        name: t.brandAjName,
        country: t.countryNicaragua,
        panel: BrandPanel.amber,
        imageAsset: 'assets/images/brands/aj.jpg',
        heritage: t.brandAjHeritage,
        facts: [
          BrandFact(label: t.factOrigin, value: t.factOriginEsteli),
          BrandFact(label: t.factFounded, value: t.factFoundedAj),
          BrandFact(label: t.factFamily, value: t.factFamilyAj),
          BrandFact(label: t.factLineCharacter, value: t.factLineCharacterAj),
        ],
        lines: [t.lineAjNewWorld, t.lineAjBellasArtes, t.lineAjEnclave, t.lineAjSanLotano],
      ),
      PartnerBrand(
        id: 'oliva',
        mono: t.brandOlivaMono,
        shortName: t.brandOlivaName,
        name: t.brandOlivaName,
        country: t.countryNicaragua,
        panel: BrandPanel.burgundy,
        imageAsset: 'assets/images/brands/oliva.jpg',
        heritage: t.brandOlivaHeritage,
        facts: [
          BrandFact(label: t.factOrigin, value: t.factOriginEsteli),
          BrandFact(label: t.factTradition, value: t.factTraditionOliva),
          BrandFact(label: t.factProduction, value: t.factProductionOliva),
          BrandFact(label: t.factLineCharacter, value: t.factLineCharacterOliva),
        ],
        lines: [t.lineOlivaSerieV, t.lineOlivaSerieG, t.lineOlivaMasterBlends, t.lineOlivaSerieO],
      ),
      PartnerBrand(
        id: 'perdomo',
        mono: t.brandPerdomoMono,
        shortName: t.brandPerdomoName,
        name: t.brandPerdomoName,
        country: t.countryNicaragua,
        panel: BrandPanel.green,
        imageAsset: 'assets/images/brands/perdomo.jpg',
        heritage: t.brandPerdomoHeritage,
        facts: [
          BrandFact(label: t.factOrigin, value: t.factOriginEsteli),
          BrandFact(label: t.factFounded, value: t.factFoundedPerdomo),
          BrandFact(label: t.factFounder, value: t.factFounderPerdomo),
          BrandFact(label: t.factFeature, value: t.factFeaturePerdomo),
        ],
        lines: [t.linePerdomoReserve, t.linePerdomoHabano, t.linePerdomoLot23],
      ),
      PartnerBrand(
        id: 'turrent',
        mono: t.brandTurrentMono,
        shortName: t.brandTurrentName,
        name: t.brandTurrentName,
        country: t.countryMexico,
        panel: BrandPanel.brown,
        imageAsset: 'assets/images/brands/turrent.jpg',
        heritage: t.brandTurrentHeritage,
        facts: [
          BrandFact(label: t.factOrigin, value: t.factOriginTurrent),
          BrandFact(label: t.factFamily, value: t.factFamilyTurrent),
          BrandFact(label: t.factLineCharacter, value: t.factLineCharacterTurrent),
        ],
        lines: [t.lineTurrent1942, t.lineTurrent1880, t.lineTurrentOrigin, t.lineTurrent1901],
      ),
    ];
  }
}
