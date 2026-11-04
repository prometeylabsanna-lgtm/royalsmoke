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
import '../../../shared/widgets/rs_insets.dart';
import '../../../shared/widgets/rs_rows.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context);
    final home = watchContent(ref).screen('home');
    return RsSafeBody(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(
          AppSizes.padX,
          24,
          AppSizes.padX,
          AppSizes.s24,
        ),
        children: [
          Text(
            textOr(home.kicker, l10n.homeKicker),
            style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32),
          ),
          const SizedBox(height: AppSizes.s12),
          SizedBox(
            width: double.infinity,
            height: 52,
            child: FittedBox(
              fit: BoxFit.scaleDown,
              alignment: Alignment.centerLeft,
              child: Text(
                textOr(home.title, l10n.homeTitle),
                maxLines: 1,
                softWrap: false,
                style: AppTextStyles.hero,
              ),
            ),
          ),
          const SizedBox(height: AppSizes.s24),
          Text(textOr(home.body, l10n.homeBody), style: AppTextStyles.body),
          const SizedBox(height: AppSizes.s16),
          RsButton(
            label: textOr(home.ctaPrimary, l10n.bookVisit),
            expand: true,
            onPressed: () => context.go('/visit'),
          ),
          const SizedBox(height: AppSizes.s12),
          RsButton(
            label: textOr(home.ctaSecondary, l10n.houseKicker),
            variant: RsButtonVariant.secondary,
            expand: true,
            onPressed: () => context.go('/house'),
          ),
          const SizedBox(height: AppSizes.s40),
          const Divider(height: 1, color: AppColors.hairline),
          RsEditorialRow(
            label: l10n.houseKicker,
            onTap: () => context.go('/house'),
          ),
          RsEditorialRow(
            label: l10n.contacts,
            onTap: () => context.go('/contacts'),
          ),
          RsEditorialRow(
            label: l10n.bookVisit,
            onTap: () => context.go('/visit'),
          ),
        ],
      ),
    );
  }
}
