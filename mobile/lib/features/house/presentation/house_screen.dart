import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_insets.dart';

class HouseScreen extends ConsumerWidget {
  const HouseScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context);
    final house = watchContent(ref).screen('house');
    final blocks = house.houseBlocks;
    return RsSafeBody(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(
          AppSizes.padX,
          24,
          AppSizes.padX,
          AppSizes.s24,
        ),
        children: [
          RsPageHeading(
            kicker: textOr(house.kicker, l10n.houseKicker),
            title: textOr(house.title, l10n.houseTitle),
          ),
          const SizedBox(height: AppSizes.s24),
          Text(
            textOr(house.body, l10n.houseBodyShort),
            style: AppTextStyles.body,
          ),
          const SizedBox(height: AppSizes.s24),
          const Divider(height: 1, color: AppColors.hairline),
          for (final block in blocks)
            _HouseBlock(
              index: block.indexLabel,
              title: block.title,
              body: block.body,
            ),
          const SizedBox(height: AppSizes.s24),
          RsButton(
            label: textOr(house.ctaPrimary, l10n.bookVisit),
            expand: true,
            onPressed: () => context.go('/visit'),
          ),
          const SizedBox(height: AppSizes.s8),
          RsButton(
            label: textOr(house.ctaSecondary, l10n.contacts),
            variant: RsButtonVariant.secondary,
            expand: true,
            onPressed: () => context.go('/contacts'),
          ),
        ],
      ),
    );
  }
}

class _HouseBlock extends StatelessWidget {
  const _HouseBlock({
    required this.index,
    required this.title,
    required this.body,
  });

  final String index;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 18),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: AppColors.hairline)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 32,
            child: Text(
              index,
              style: AppTextStyles.kicker.copyWith(color: AppColors.gold),
            ),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: AppTextStyles.title.copyWith(
                    fontSize: 18,
                    letterSpacing: 18 * 0.12,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  body,
                  style: AppTextStyles.body.copyWith(
                    color: AppColors.textMuted,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
