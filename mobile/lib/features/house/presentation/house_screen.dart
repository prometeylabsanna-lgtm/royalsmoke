import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_chrome.dart';

class HouseScreen extends StatelessWidget {
  const HouseScreen({super.key});

  static const _blocks = [
    ('01', 'Сервіс', 'Консультації щодо брендів, історії та зберігання.'),
    ('02', 'B2B', 'Співпраця із закладами та професійними партнерами.'),
    ('03', 'Візит', 'Знайомство з домом за попереднім записом.'),
  ];

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
      children: [
        const RsPageHeading(kicker: 'Про дім', title: 'Дім\nRoyal Smoke'),
        const SizedBox(height: AppSizes.s24),
        Text(
          'Royal Smoke — дім, що представляє в Україні родинні бренди з багаторічною історією. Тут можна дізнатися про походження брендів і познайомитися з колекцією під час візиту.',
          style: AppTextStyles.body,
        ),
        const SizedBox(height: AppSizes.s24),
        ClipRRect(
          borderRadius: BorderRadius.circular(AppSizes.radiusSearch),
          child: SizedBox(
            height: 220,
            width: double.infinity,
            child: Image.asset(
              'assets/images/home/house.jpg',
              fit: BoxFit.cover,
            ),
          ),
        ),
        const SizedBox(height: AppSizes.s24),
        const Divider(height: 1, color: AppColors.hairline),
        for (final block in _blocks) _HouseBlock(index: block.$1, title: block.$2, body: block.$3),
        const SizedBox(height: AppSizes.s24),
        RsButton(label: 'Забронювати візит', expand: true, onPressed: () => context.go('/house/visit')),
        const SizedBox(height: AppSizes.s8),
        RsButton(
          label: 'Контакти',
          variant: RsButtonVariant.secondary,
          expand: true,
          onPressed: () => context.go('/more/contacts'),
        ),
      ],
    );
  }
}

class _HouseBlock extends StatelessWidget {
  const _HouseBlock({required this.index, required this.title, required this.body});

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
            child: Text(index, style: AppTextStyles.kicker.copyWith(color: AppColors.gold)),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title.toUpperCase(), style: AppTextStyles.brandName.copyWith(letterSpacing: 15 * 0.14)),
                const SizedBox(height: 4),
                Text(body, style: AppTextStyles.body.copyWith(fontSize: 14, color: AppColors.textMuted)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
