import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/brands/data/partner_catalog.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_brand_pattern.dart';
import '../../../shared/widgets/rs_rows.dart';

class BrandDetailScreen extends StatefulWidget {
  const BrandDetailScreen({super.key, required this.brandId});

  final String brandId;

  @override
  State<BrandDetailScreen> createState() => _BrandDetailScreenState();
}

class _BrandDetailScreenState extends State<BrandDetailScreen> {
  bool _saved = false;

  @override
  Widget build(BuildContext context) {
    final matches = PartnerCatalog.brands.where((b) => b.id == widget.brandId);
    if (matches.isEmpty) {
      return const Center(child: Text('Бренд не знайдено'));
    }
    final item = matches.first;

    final panelHeight = (MediaQuery.sizeOf(context).height * 0.38).clamp(240.0, 330.0);
    return ListView(
      padding: EdgeInsets.zero,
      children: [
        SizedBox(
          height: panelHeight,
          child: ClipRect(
            child: RsBrandLetterPanel(
              brand: item,
              patternWord: 'ROYAL',
              fontSize: 18,
              rowCount: 22,
              extendLower: true,
              child: Stack(
                fit: StackFit.expand,
                clipBehavior: Clip.hardEdge,
                children: [
                  const ColoredBox(color: Color(0x66100D0C)),
                  Align(
                    alignment: Alignment.topLeft,
                    child: SafeArea(
                      bottom: false,
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        child: Row(
                          children: [
                            TextButton.icon(
                              onPressed: () => context.go('/brands'),
                              icon: const Icon(Icons.chevron_left, color: AppColors.seashell),
                              label: Text('БРЕНДИ', style: AppTextStyles.back),
                            ),
                            const Spacer(),
                            IconButton(
                              onPressed: () => setState(() => _saved = !_saved),
                              icon: Icon(
                                _saved ? Icons.bookmark : Icons.bookmark_border,
                                color: AppColors.seashell,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  Center(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 48, AppSizes.padX, 24),
                      child: RsBrandTitle(
                        name: item.name,
                        style: AppTextStyles.hero.copyWith(
                          fontSize: 48,
                          letterSpacing: 48 * 0.16,
                          height: 1.08,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(AppSizes.padX, 32, AppSizes.padX, 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(item.country.toUpperCase(), style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
              const SizedBox(height: AppSizes.s12),
              Text(item.name.toUpperCase(), style: AppTextStyles.title.copyWith(letterSpacing: 28 * 0.24)),
              const SizedBox(height: AppSizes.s16),
              Text(item.heritage, style: AppTextStyles.body),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(AppSizes.padX, 40, AppSizes.padX, 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('КОРОТКО', style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
              const SizedBox(height: AppSizes.s12),
              const Divider(height: 1, color: AppColors.hairline),
              for (final fact in item.facts) RsFactRow(label: fact.label, value: fact.value),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(AppSizes.padX, 40, AppSizes.padX, 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('ЛІНІЙКИ', style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
              const SizedBox(height: AppSizes.s12),
              const Divider(height: 1, color: AppColors.hairline),
              for (var i = 0; i < item.lines.length; i++) RsLineRow(index: i + 1, title: item.lines[i]),
              const SizedBox(height: AppSizes.s40),
              GestureDetector(
                onTap: () => context.go('/brands'),
                child: Text('УСІ БРЕНДИ', style: AppTextStyles.link),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
