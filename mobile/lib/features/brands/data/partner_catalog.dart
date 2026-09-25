import '../domain/partner_brand.dart';

/// Чернетка з прототипу. Пізніше ці записи прийдуть з адмінки.
abstract final class PartnerCatalog {
  static const List<PartnerBrand> brands = [
    PartnerBrand(
      id: 'aj',
      mono: 'AJ',
      shortName: 'AJ',
      name: 'AJ Fernandez',
      country: 'Нікарагуа',
      panel: BrandPanel.amber,
      imageAsset: 'assets/images/brands/aj.jpg',
      heritage:
          'Абдель Фернандес — представник четвертого покоління кубинської тютюнової родини. Власну фабрику в Естелі заснував на початку 2000-х; компанія працює з власними плантаціями в кількох регіонах Нікарагуа.',
      facts: [
        BrandFact(label: 'Походження', value: 'Естелі, Нікарагуа'),
        BrandFact(label: 'Засновано', value: 'Початок 2000-х'),
        BrandFact(label: 'Родина', value: 'Фернандес, кубинське коріння'),
        BrandFact(label: 'Характер ліній', value: 'Насичені, щільні бленди'),
      ],
      lines: ['New World', 'Bellas Artes', 'Enclave', 'San Lotano'],
    ),
    PartnerBrand(
      id: 'oliva',
      mono: 'O',
      shortName: 'Oliva',
      name: 'Oliva',
      country: 'Нікарагуа',
      panel: BrandPanel.burgundy,
      imageAsset: 'assets/images/brands/oliva.jpg',
      heritage:
          'Родина Олива вирощує тютюн з кінця XIX століття, починаючи з провінції Пінар-дель-Ріо на Кубі. Після еміграції виробництво зосередилося в Нікарагуа, де розташовані основні поля та фабрика бренду.',
      facts: [
        BrandFact(label: 'Походження', value: 'Естелі, Нікарагуа'),
        BrandFact(label: 'Традиція', value: 'З кінця XIX ст., Куба'),
        BrandFact(label: 'Сировина', value: 'Власні поля в долині Хамастран'),
        BrandFact(label: 'Характер ліній', value: 'Від збалансованих до насичених'),
      ],
      lines: ['Serie V', 'Serie G', 'Master Blends', 'Serie O'],
    ),
    PartnerBrand(
      id: 'perdomo',
      mono: 'P',
      shortName: 'Perdomo',
      name: 'Perdomo',
      country: 'Нікарагуа',
      panel: BrandPanel.green,
      imageAsset: 'assets/images/brands/perdomo.jpg',
      heritage:
          'Бренд засновано в Маямі на початку 1990-х. Згодом виробництво перенесено до Естелі, де компанія вибудувала повний цикл — від власних полів до фабрики та витримки сировини.',
      facts: [
        BrandFact(label: 'Походження', value: 'Естелі, Нікарагуа'),
        BrandFact(label: 'Засновано', value: '1990-ті, Маямі'),
        BrandFact(label: 'Засновник', value: 'Нік Пердомо'),
        BrandFact(label: 'Особливість', value: 'Тривала витримка сировини'),
      ],
      lines: ['Reserve 10th Anniversary', 'Habano', 'Lot 23'],
    ),
    PartnerBrand(
      id: 'turrent',
      mono: 'CT',
      shortName: 'Casa Turrent',
      name: 'Casa Turrent',
      country: 'Мексика',
      panel: BrandPanel.brown,
      imageAsset: 'assets/images/brands/turrent.jpg',
      heritage:
          'Мексиканський бренд родини Турренте. Вирощування тютюну в долині Сан-Андрес, штат Веракрус; власний покривний лист мексиканського походження.',
      facts: [
        BrandFact(label: 'Походження', value: 'Сан-Андрес, Мексика'),
        BrandFact(label: 'Родина', value: 'Турренте'),
        BrandFact(label: 'Характер ліній', value: 'Насичений покривний лист, довгий післясмак'),
      ],
      lines: ['Лінійка 1', 'Лінійка 2', 'Лінійка 3'],
    ),
  ];
}
