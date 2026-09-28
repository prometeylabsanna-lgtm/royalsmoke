import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/brands/presentation/saved_brands_provider.dart';
import '../../../features/content/data/fallback_bundle.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_cover_image.dart';
import '../../../shared/widgets/rs_rows.dart';

class MoreScreen extends ConsumerWidget {
  const MoreScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = watchContent(ref);
    final savedCount = ref.watch(savedBrandsProvider).length;
    final sealUrl = content.settings.appSealUrl;
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
      children: [
        const RsPageHeading(kicker: 'Royal Smoke', title: 'Ще'),
        const SizedBox(height: AppSizes.s24),
        const Divider(height: 1, color: AppColors.hairline),
        RsEditorialRow(
          label: 'Збережені бренди',
          leading: const Icon(Icons.bookmark_border, color: AppColors.gold, size: 18),
          trailing: Text(
            '$savedCount',
            style: AppTextStyles.body.copyWith(fontSize: 13, color: AppColors.textMuted),
          ),
          onTap: () => context.go('/offline'),
        ),
        RsEditorialRow(label: 'Контакти', onTap: () => context.push('/more/contacts')),
        RsEditorialRow(
          label: content.page('privacy')?.title ?? 'Політика конфіденційності',
          onTap: () => context.push('/more/page/privacy'),
        ),
        RsEditorialRow(
          label: content.page('terms')?.title ?? 'Умови',
          onTap: () => context.push('/more/page/terms'),
        ),
        RsEditorialRow(
          label: content.page('age')?.title ?? 'Вікова політика',
          onTap: () => context.push('/more/page/age'),
        ),
        RsEditorialRow(
          label: content.page('about')?.title ?? 'Про застосунок',
          onTap: () => context.push('/more/page/about'),
        ),
        const SizedBox(height: 48),
        Column(
          children: [
            if (sealUrl.isNotEmpty)
              ClipOval(
                child: SizedBox(
                  width: 44,
                  height: 44,
                  child: RsCoverImage(imageUrl: sealUrl, assetFallback: 'assets/images/branding/app_icon_master.png'),
                ),
              )
            else
              const RsSeal(size: 44),
            const SizedBox(height: AppSizes.s12),
            Text(content.settings.appVersion, style: AppTextStyles.kicker),
          ],
        ),
      ],
    );
  }
}

class InfoPageScreen extends ConsumerWidget {
  const InfoPageScreen({super.key, required this.pageId});

  final String pageId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = watchContent(ref);
    final page = content.page(pageId) ?? buildFallbackBundle().page(pageId);
    final title = page?.title ?? 'Документ';
    final body = page?.body ?? content.settings.appBlurb;
    final viewH = MediaQuery.sizeOf(context).height;
    final topInset = MediaQuery.paddingOf(context).top;
    final bottomInset = MediaQuery.paddingOf(context).bottom;
    final minContentH = (viewH - topInset - bottomInset - 120).clamp(420.0, 900.0);

    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 8, AppSizes.padX, AppSizes.s40),
      child: ConstrainedBox(
        constraints: BoxConstraints(minHeight: minContentH),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            RsBackBar(
              label: 'Ще',
              onPressed: () {
                if (context.canPop()) {
                  context.pop();
                } else {
                  context.go('/more');
                }
              },
            ),
            RsPageHeading(
              kicker: 'Royal Smoke',
              title: title,
              compactTitle: true,
            ),
            const SizedBox(height: 36),
            Text(
              body,
              style: AppTextStyles.body.copyWith(height: 1.65, fontSize: 15),
            ),
            const SizedBox(height: AppSizes.s40),
          ],
        ),
      ),
    );
  }
}
