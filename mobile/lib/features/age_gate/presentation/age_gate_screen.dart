import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/l10n/app_locale.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_insets.dart';

class AgeGateScreen extends ConsumerWidget {
  const AgeGateScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context);
    final age = watchContent(ref).screen('age');
    final bottom = rsBottomInset(context);
    return Scaffold(
      backgroundColor: AppColors.bark,
      body: RsSafeBody(
        child: Stack(
          children: [
            const Positioned.fill(child: ColoredBox(color: Color(0x8C0A0705))),
            Center(
              child: Opacity(
                opacity: 0.35,
                child: Padding(
                  padding: const EdgeInsets.only(left: 22 * 0.32),
                  child: Text(
                    l10n.splashTitle,
                    style: TextStyle(
                      fontFamily: AppTextStyles.family,
                      fontSize: 22,
                      fontWeight: FontWeight.w600,
                      letterSpacing: 22 * 0.32,
                      color: AppColors.seashell,
                    ),
                  ),
                ),
              ),
            ),
            Align(
              alignment: Alignment.bottomCenter,
              child: Container(
                width: double.infinity,
                padding: EdgeInsets.fromLTRB(
                  AppSizes.padX,
                  12,
                  AppSizes.padX,
                  24 + bottom,
                ),
                decoration: const BoxDecoration(
                  color: AppColors.coffee,
                  borderRadius: BorderRadius.vertical(
                    top: Radius.circular(AppSizes.radiusSheet),
                  ),
                  border: Border(top: BorderSide(color: Color(0x1AFCF2EE))),
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Container(
                        width: 36,
                        height: 4,
                        decoration: BoxDecoration(
                          color: const Color(0x40FCF2EE),
                          borderRadius: BorderRadius.circular(2),
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                    Text(
                      textOr(age.kicker, l10n.ageKicker).toUpperCase(),
                      style: AppTextStyles.kicker.copyWith(
                        letterSpacing: 11 * 0.32,
                      ),
                    ),
                    const SizedBox(height: AppSizes.s24),
                    Text(
                      textOr(age.title, l10n.ageTitle).toUpperCase(),
                      style: TextStyle(
                        fontFamily: AppTextStyles.family,
                        fontSize: 24,
                        fontWeight: FontWeight.w600,
                        height: 1.2,
                        letterSpacing: 24 * 0.2,
                        color: AppColors.seashell,
                      ),
                    ),
                    const SizedBox(height: AppSizes.s24),
                    Text(
                      textOr(age.body, l10n.ageBodyShort),
                      style: AppTextStyles.body,
                    ),
                    const SizedBox(height: AppSizes.s24),
                    Text(
                      textOr(age.legalNote, l10n.ageLegal),
                      style: AppTextStyles.body.copyWith(
                        fontSize: 13,
                        color: AppColors.textMuted,
                      ),
                    ),
                    const SizedBox(height: 32),
                    RsButton(
                      label: textOr(age.confirmLabel, l10n.ageConfirm),
                      variant: RsButtonVariant.secondary,
                      expand: true,
                      onPressed: () => context.go('/home'),
                    ),
                    TextButton(
                      onPressed: () => context.go('/splash'),
                      style: TextButton.styleFrom(
                        minimumSize: const Size(double.infinity, 48),
                        foregroundColor: AppColors.textMuted,
                      ),
                      child: Text(
                        textOr(age.ctaSecondary, l10n.ageExit),
                        style: TextStyle(
                          fontFamily: AppTextStyles.family,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 12 * 0.24,
                          color: AppColors.textMuted,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
