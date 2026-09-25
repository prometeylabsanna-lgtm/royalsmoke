import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_chrome.dart';

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 8, AppSizes.padX, AppSizes.s24),
      children: [
        RsBackBar(label: 'Ще', onPressed: () => context.go('/more')),
        const RsPageHeading(kicker: 'Дім Royal Smoke', title: 'Контакти'),
        const SizedBox(height: 20),
        Container(
          height: 190,
          alignment: Alignment.bottomRight,
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.coffee,
            borderRadius: BorderRadius.circular(AppSizes.radiusSearch),
          ),
          child: Text('МАПА', style: AppTextStyles.kicker),
        ),
        const SizedBox(height: 20),
        const Divider(height: 1, color: AppColors.hairline),
        const _ContactBlock(label: 'Адреса', value: 'вул. Назва, 00, Київ', action: 'Прокласти маршрут'),
        const _ContactBlock(label: 'Телефон', value: '+380 00 000 00 00', action: 'Зателефонувати'),
        const _ContactBlock(label: 'Години', value: 'Пн–Нд · 11:00–22:00'),
      ],
    );
  }
}

class _ContactBlock extends StatelessWidget {
  const _ContactBlock({required this.label, required this.value, this.action});

  final String label;
  final String value;
  final String? action;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 16),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: AppColors.hairline)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label.toUpperCase(), style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.24)),
          const SizedBox(height: 6),
          Text(value, style: AppTextStyles.body),
          if (action != null) ...[
            const SizedBox(height: 6),
            Text(action!.toUpperCase(), style: AppTextStyles.link.copyWith(color: AppColors.gold, decoration: TextDecoration.none)),
          ],
        ],
      ),
    );
  }
}
