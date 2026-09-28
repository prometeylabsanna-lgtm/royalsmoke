import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../core/constants/app_copy.dart';
import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_venue_map.dart';

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});

  Future<void> _openMaps() async {
    final uri = Uri.parse(
      'https://maps.apple.com/?ll=${AppCopy.contactLat},${AppCopy.contactLng}'
      '&q=${Uri.encodeComponent(AppCopy.contactAddress)}',
    );
    await launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  Future<void> _call() async {
    final digits = AppCopy.contactPhone.replaceAll(RegExp(r'[^\d+]'), '');
    final uri = Uri(scheme: 'tel', path: digits);
    await launchUrl(uri);
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 8, AppSizes.padX, AppSizes.s24),
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
        const RsPageHeading(kicker: 'Дім Royal Smoke', title: 'Контакти'),
        const SizedBox(height: 12),
        Text(AppCopy.appBlurb, style: AppTextStyles.body),
        const SizedBox(height: 20),
        const RsVenueMap(),
        const SizedBox(height: 20),
        const Divider(height: 1, color: AppColors.hairline),
        _ContactBlock(
          label: 'Адреса',
          value: AppCopy.contactAddress,
          action: 'Прокласти маршрут',
          onAction: _openMaps,
        ),
        _ContactBlock(
          label: 'Телефон',
          value: AppCopy.contactPhone,
          action: 'Зателефонувати',
          onAction: _call,
        ),
        const _ContactBlock(label: 'Години', value: AppCopy.contactHours),
      ],
    );
  }
}

class _ContactBlock extends StatelessWidget {
  const _ContactBlock({
    required this.label,
    required this.value,
    this.action,
    this.onAction,
  });

  final String label;
  final String value;
  final String? action;
  final VoidCallback? onAction;

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
            GestureDetector(
              onTap: onAction,
              child: Text(
                action!.toUpperCase(),
                style: AppTextStyles.link.copyWith(
                  color: AppColors.gold,
                  decoration: TextDecoration.none,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
