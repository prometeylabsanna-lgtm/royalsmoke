import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_insets.dart';

class ContactsScreen extends ConsumerWidget {
  const ContactsScreen({super.key});

  Future<void> _call(String phone) async {
    final digits = phone.replaceAll(RegExp(r'[^\d+]'), '');
    if (digits.isEmpty) return;
    final uri = Uri(scheme: 'tel', path: digits);
    await launchUrl(uri);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context);
    final settings = watchContent(ref).settings;
    final phone = settings.contactPhone.trim();
    final hours = settings.contactHours.trim();
    final hasDetails = phone.isNotEmpty || hours.isNotEmpty;

    return RsSafeBody(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(
          AppSizes.padX,
          24,
          AppSizes.padX,
          AppSizes.s24,
        ),
        children: [
          RsPageHeading(kicker: l10n.appName, title: l10n.contacts),
          if (hasDetails) ...[
            const SizedBox(height: 20),
            const Divider(height: 1, color: AppColors.hairline),
            if (phone.isNotEmpty)
              _ContactBlock(
                label: l10n.phoneLabel,
                value: phone,
                action: l10n.call,
                onAction: () => _call(phone),
              ),
            if (hours.isNotEmpty)
              _ContactBlock(label: l10n.hoursLabel, value: hours),
          ],
        ],
      ),
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
          Text(
            label.toUpperCase(),
            style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.24),
          ),
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
