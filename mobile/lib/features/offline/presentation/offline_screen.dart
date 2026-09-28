import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../features/brands/presentation/saved_brands_provider.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_chrome.dart';

class OfflineScreen extends ConsumerWidget {
  const OfflineScreen({super.key});

  String _formatDate(DateTime dt) {
    final d = dt.day.toString().padLeft(2, '0');
    final m = dt.month.toString().padLeft(2, '0');
    return '$d.$m.${dt.year}';
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final saved = ref.watch(savedBrandListProvider);
    final updatedAt = watchContent(ref).updatedAt;
    final updatedLabel =
        updatedAt == null ? 'Локальний каталог' : 'Оновлено ${_formatDate(updatedAt)}';
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
      children: [
        const RsPageHeading(
          kicker: 'Довідник',
          title: 'Офлайн',
          subtitle: 'Збережений довідник брендів',
        ),
        const SizedBox(height: AppSizes.s24),
        Row(
          children: [
            const RsOfflineChip(),
            const Spacer(),
            Text(
              updatedLabel,
              style: const TextStyle(
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
        if (saved.isEmpty)
          const Padding(
            padding: EdgeInsets.only(top: 48),
            child: Text(
              'Поки немає збережених брендів.\nДодайте їх закладкою на картці бренду.',
              style: TextStyle(
                fontFamily: 'Fixel Display',
                fontSize: 15,
                height: 1.5,
                color: AppColors.textMuted,
              ),
            ),
          )
        else
          for (final brand in saved)
            RsOfflineBrandRow(
              brand: brand,
              onTap: () => context.go('/brands/${brand.id}'),
            ),
      ],
    );
  }
}
