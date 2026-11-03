import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/brands/presentation/saved_brands_provider.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_brand_pattern.dart';
import '../../../shared/widgets/rs_insets.dart';
import '../../../shared/widgets/rs_rows.dart';

class BrandDetailScreen extends ConsumerWidget {
  const BrandDetailScreen({super.key, required this.brandId});

  final String brandId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context);
    final content = watchContent(ref);
    final item = content.brandById(brandId);
    if (item == null) {
      return RsSafeBody(
        child: ColoredBox(
          color: AppColors.bark,
          child: Center(child: Text(l10n.brandNotFound)),
        ),
      );
    }
    final saved = ref.watch(savedBrandsProvider).contains(brandId);

    final panelHeight = (MediaQuery.sizeOf(context).height * 0.38).clamp(
      240.0,
      330.0,
    );
    return RsSafeBody(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          SizedBox(
            height: panelHeight,
            child: ClipRect(
              child: RsBrandLetterPanel(
                brand: item,
                patternWord: l10n.patternRoyal,
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
                                icon: const Icon(
                                  Icons.chevron_left,
                                  color: AppColors.seashell,
                                ),
                                label: Text(
                                  l10n.brandsBack,
                                  style: AppTextStyles.back,
                                ),
                              ),
                              const Spacer(),
                              IconButton(
                                onPressed: () => ref
                                    .read(savedBrandsProvider.notifier)
                                    .toggle(brandId),
                                icon: Icon(
                                  saved
                                      ? Icons.bookmark
                                      : Icons.bookmark_border,
                                  color: AppColors.gold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Align(
                      alignment: Alignment.bottomCenter,
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(24, 0, 24, 28),
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
            padding: const EdgeInsets.fromLTRB(
              AppSizes.padX,
              32,
              AppSizes.padX,
              0,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item.country.toUpperCase(),
                  style: AppTextStyles.kicker.copyWith(
                    letterSpacing: 11 * 0.32,
                  ),
                ),
                const SizedBox(height: AppSizes.s12),
                Text(
                  item.name.toUpperCase(),
                  style: AppTextStyles.title.copyWith(letterSpacing: 28 * 0.24),
                ),
                const SizedBox(height: AppSizes.s16),
                Text(item.heritage, style: AppTextStyles.body),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSizes.padX,
              40,
              AppSizes.padX,
              0,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.factsKicker,
                  style: AppTextStyles.kicker.copyWith(
                    letterSpacing: 11 * 0.32,
                  ),
                ),
                const SizedBox(height: AppSizes.s12),
                const Divider(height: 1, color: AppColors.hairline),
                for (final fact in item.facts)
                  RsFactRow(label: fact.label, value: fact.value),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSizes.padX,
              40,
              AppSizes.padX,
              16,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.linesKicker,
                  style: AppTextStyles.kicker.copyWith(
                    letterSpacing: 11 * 0.32,
                  ),
                ),
                const SizedBox(height: AppSizes.s12),
                const Divider(height: 1, color: AppColors.hairline),
                for (var i = 0; i < item.lines.length; i++)
                  RsLineRow(index: i + 1, title: item.lines[i]),
                const SizedBox(height: AppSizes.s40),
                GestureDetector(
                  onTap: () => context.go('/brands'),
                  child: Text(l10n.allBrands, style: AppTextStyles.link),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
