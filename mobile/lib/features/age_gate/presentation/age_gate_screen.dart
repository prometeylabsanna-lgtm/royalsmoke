import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_copy.dart';
import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_button.dart';

class AgeGateScreen extends StatelessWidget {
  const AgeGateScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final bottom = MediaQuery.paddingOf(context).bottom;
    return Scaffold(
      backgroundColor: AppColors.bark,
      body: Stack(
        children: [
          const Positioned.fill(child: ColoredBox(color: Color(0x8C0A0705))),
          Center(
            child: Opacity(
              opacity: 0.35,
              child: Padding(
                padding: const EdgeInsets.only(left: 22 * 0.32),
                child: Text(
                  'ROYAL SMOKE',
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
              padding: EdgeInsets.fromLTRB(AppSizes.padX, 12, AppSizes.padX, 24 + bottom),
              decoration: const BoxDecoration(
                color: AppColors.coffee,
                borderRadius: BorderRadius.vertical(top: Radius.circular(AppSizes.radiusSheet)),
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
                  Text(AppCopy.ageKicker.toUpperCase(), style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
                  const SizedBox(height: AppSizes.s24),
                  Text(
                    AppCopy.ageTitle.toUpperCase(),
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
                  Text(AppCopy.ageBody, style: AppTextStyles.body),
                  const SizedBox(height: AppSizes.s24),
                  Text(
                    AppCopy.ageLegal,
                    style: AppTextStyles.body.copyWith(fontSize: 13, color: AppColors.textMuted),
                  ),
                  const SizedBox(height: 32),
                  RsButton(
                    label: AppCopy.ageConfirm,
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
                      'ВИЙТИ',
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
    );
  }
}
