import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_cover_image.dart';
import '../../../shared/widgets/rs_insets.dart';
import '../../../shared/widgets/rs_rows.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context);
    final home = watchContent(ref).screen('home');
    final media = MediaQuery.of(context);
    final screenH = media.size.height;
    final heroHeight = (screenH * 0.34).clamp(200.0, 300.0);
    return RsSafeBody(
      child: ListView(
        padding: const EdgeInsets.only(bottom: AppSizes.s24),
        children: [
          SizedBox(
            height: heroHeight,
            child: Stack(
              fit: StackFit.expand,
              children: [
                RsCoverImage(
                  imageUrl: home.heroImageUrl,
                  assetFallback: home.heroAssetFallback.isEmpty
                      ? 'assets/images/home/hero.jpg'
                      : home.heroAssetFallback,
                ),
                const DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [Color(0x0017110D), AppColors.bark],
                      stops: [0.45, 1],
                    ),
                  ),
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSizes.padX,
              8,
              AppSizes.padX,
              0,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  textOr(home.kicker, l10n.homeKicker),
                  style: AppTextStyles.kicker.copyWith(
                    letterSpacing: 11 * 0.32,
                  ),
                ),
                const SizedBox(height: AppSizes.s12),
                Text(
                  textOr(home.title, l10n.homeTitle),
                  style: AppTextStyles.hero,
                ),
                const SizedBox(height: AppSizes.s24),
                Text(
                  textOr(home.body, l10n.homeBody),
                  style: AppTextStyles.body,
                ),
                const SizedBox(height: AppSizes.s16),
                RsButton(
                  label: l10n.bookVisit,
                  expand: true,
                  onPressed: () => context.go('/visit'),
                ),
                const SizedBox(height: AppSizes.s12),
                RsButton(
                  label: l10n.houseTab,
                  variant: RsButtonVariant.secondary,
                  expand: true,
                  onPressed: () => context.go('/house'),
                ),
              ],
            ),
          ),
          const SizedBox(height: AppSizes.s40),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: AppSizes.padX),
            child: Column(
              children: [
                const Divider(height: 1, color: AppColors.hairline),
                RsEditorialRow(
                  label: l10n.houseKicker,
                  onTap: () => context.go('/house'),
                ),
                RsEditorialRow(
                  label: l10n.contacts,
                  onTap: () => context.go('/more/contacts'),
                ),
                RsEditorialRow(
                  label: l10n.bookVisit,
                  onTap: () => context.go('/visit'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
