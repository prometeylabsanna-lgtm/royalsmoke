import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_copy.dart';
import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_rows.dart';

class MoreScreen extends StatelessWidget {
  const MoreScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
      children: [
        const RsPageHeading(kicker: 'Royal Smoke', title: 'Ще'),
        const SizedBox(height: AppSizes.s24),
        const Divider(height: 1, color: AppColors.hairline),
        RsEditorialRow(
          label: 'Збережені бренди',
          leading: const Icon(Icons.bookmark_border, color: AppColors.gold, size: 18),
          trailing: Text('2', style: AppTextStyles.body.copyWith(fontSize: 13, color: AppColors.textMuted)),
          onTap: () => context.go('/brands'),
        ),
        RsEditorialRow(label: 'Контакти', onTap: () => context.go('/more/contacts')),
        RsEditorialRow(label: 'Політика конфіденційності', onTap: () => context.go('/more/page/privacy')),
        RsEditorialRow(label: 'Умови', onTap: () => context.go('/more/page/terms')),
        RsEditorialRow(label: 'Вікова політика', onTap: () => context.go('/more/page/age')),
        RsEditorialRow(label: 'Про застосунок', onTap: () => context.go('/more/page/about')),
        const SizedBox(height: 48),
        Column(
          children: [
            const RsSeal(size: 44),
            const SizedBox(height: AppSizes.s12),
            Text(AppCopy.appVersion, style: AppTextStyles.kicker),
          ],
        ),
      ],
    );
  }
}

class InfoPageScreen extends StatelessWidget {
  const InfoPageScreen({super.key, required this.pageId});

  final String pageId;

  static const _titles = {
    'privacy': 'Політика конфіденційності',
    'terms': 'Умови',
    'age': 'Вікова політика',
    'about': 'Про застосунок',
  };

  @override
  Widget build(BuildContext context) {
    final title = _titles[pageId] ?? 'Документ';
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 8, AppSizes.padX, AppSizes.s24),
      children: [
        RsBackBar(label: 'Ще', onPressed: () => context.go('/more')),
        RsPageHeading(kicker: 'Royal Smoke', title: title),
        const SizedBox(height: AppSizes.s24),
        Text(
          pageId == 'age'
              ? 'Вміст довідника призначений для осіб, яким виповнилося 21 рік. Застосунок не продає продукцію.'
              : 'Текст цього розділу зʼявиться з адмінки. Зараз це довідкова сторінка без продажу.',
          style: AppTextStyles.body,
        ),
      ],
    );
  }
}
