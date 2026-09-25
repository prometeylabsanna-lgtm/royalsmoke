import 'package:flutter/material.dart';

import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';

enum RsButtonVariant { primary, secondary, ghost }

class RsButton extends StatelessWidget {
  const RsButton({
    super.key,
    required this.label,
    this.onPressed,
    this.variant = RsButtonVariant.primary,
    this.loading = false,
    this.expand = false,
  });

  final String label;
  final VoidCallback? onPressed;
  final RsButtonVariant variant;
  final bool loading;
  final bool expand;

  @override
  Widget build(BuildContext context) {
    final enabled = onPressed != null && !loading;
    final child = loading
        ? SizedBox(
            width: 18,
            height: 18,
            child: CircularProgressIndicator(
              strokeWidth: 1.6,
              color: variant == RsButtonVariant.primary
                  ? AppColors.bark
                  : AppColors.gold,
            ),
          )
        : Text(
            label.toUpperCase(),
            style: AppTextStyles.button.copyWith(color: _foreground),
          );

    final button = SizedBox(
      height: variant == RsButtonVariant.ghost ? AppSizes.tap : AppSizes.buttonHeight,
      child: switch (variant) {
        RsButtonVariant.primary => FilledButton(
            onPressed: enabled ? onPressed : null,
            style: FilledButton.styleFrom(
              backgroundColor: AppColors.gold,
              disabledBackgroundColor: AppColors.gold.withValues(alpha: 0.4),
              foregroundColor: AppColors.bark,
              elevation: 0,
              padding: const EdgeInsets.symmetric(horizontal: 32),
              shape: const StadiumBorder(),
            ),
            child: child,
          ),
        RsButtonVariant.secondary => OutlinedButton(
            onPressed: enabled ? onPressed : null,
            style: OutlinedButton.styleFrom(
              foregroundColor: AppColors.gold,
              side: const BorderSide(color: AppColors.gold),
              padding: const EdgeInsets.symmetric(horizontal: 32),
              shape: const StadiumBorder(),
            ),
            child: child,
          ),
        RsButtonVariant.ghost => TextButton(
            onPressed: enabled ? onPressed : null,
            style: TextButton.styleFrom(
              foregroundColor: AppColors.seashell,
              padding: const EdgeInsets.symmetric(horizontal: 20),
            ),
            child: child,
          ),
      },
    );

    if (!expand) return button;
    return SizedBox(width: double.infinity, child: button);
  }

  Color get _foreground => switch (variant) {
        RsButtonVariant.primary => AppColors.bark,
        RsButtonVariant.secondary => AppColors.gold,
        RsButtonVariant.ghost => AppColors.seashell,
      };
}
