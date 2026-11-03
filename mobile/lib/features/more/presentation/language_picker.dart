import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/l10n/app_locale.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';

class LanguagePicker extends ConsumerWidget {
  const LanguagePicker({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final current = apiLanguageCode(ref.watch(appLocaleProvider));
    return Wrap(
      spacing: AppSizes.s8,
      runSpacing: AppSizes.s8,
      children: [
        for (final option in appLanguageOptions)
          _LanguageChip(
            label: option.$2,
            selected: option.$1 == current,
            onTap: () => ref.read(appLocaleProvider.notifier).select(option.$1),
          ),
      ],
    );
  }
}

class _LanguageChip extends StatelessWidget {
  const _LanguageChip({required this.label, required this.selected, required this.onTap});

  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final color = selected ? AppColors.gold : AppColors.textMuted;
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSizes.radiusChip),
        child: ConstrainedBox(
          constraints: const BoxConstraints(minHeight: AppSizes.tap, minWidth: AppSizes.tap),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            alignment: Alignment.center,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(AppSizes.radiusChip),
              border: Border.all(color: selected ? AppColors.gold : AppColors.hairline),
            ),
            child: Text(
              label,
              style: AppTextStyles.body.copyWith(fontSize: 14, height: 1.2, color: color),
            ),
          ),
        ),
      ),
    );
  }
}
