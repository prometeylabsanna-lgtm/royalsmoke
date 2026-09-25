import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../features/brands/data/partner_catalog.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_chrome.dart';

class OfflineScreen extends StatelessWidget {
  const OfflineScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
      children: [
        const RsPageHeading(
          kicker: 'Довідник',
          title: 'Офлайн',
          subtitle: 'Збережений довідник брендів',
        ),
        const SizedBox(height: AppSizes.s24),
        const Row(
          children: [
            RsOfflineChip(),
            Spacer(),
            Text(
              'Оновлено 24.09.2026',
              style: TextStyle(
                fontFamily: 'Fixel Display',
                fontSize: 11,
                letterSpacing: 1.3,
                color: AppColors.textMuted,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppSizes.s24),
        const Divider(height: 1, color: AppColors.gold),
        const SizedBox(height: AppSizes.s8),
        const Divider(height: 1, color: AppColors.hairline),
        for (final brand in PartnerCatalog.brands)
          RsOfflineBrandRow(
            brand: brand,
            onTap: () => context.go('/brands/${brand.id}'),
          ),
      ],
    );
  }
}
