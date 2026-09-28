import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_cover_image.dart';
import '../../../shared/widgets/rs_rows.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final content = watchContent(ref);
    final home = content.screen('home');
    final brands = content.brands;
    final media = MediaQuery.of(context);
    final screenH = media.size.height;
    final heroHeight = (screenH * 0.34).clamp(200.0, 300.0);
    return ListView(
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
          padding: const EdgeInsets.fromLTRB(AppSizes.padX, 8, AppSizes.padX, 0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                home.kicker.isEmpty ? 'ДІМ БРЕНДУ' : home.kicker,
                style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32),
              ),
              const SizedBox(height: AppSizes.s12),
              Text(
                home.title.isEmpty ? 'ROYAL\nSMOKE' : home.title,
                style: AppTextStyles.hero,
              ),
              const SizedBox(height: AppSizes.s24),
              Text(
                home.body.isEmpty ? 'Довідник дому бренду та партнерів' : home.body,
                style: AppTextStyles.body,
              ),
              const SizedBox(height: AppSizes.s16),
              Builder(
                builder: (context) {
                  final brandsBtn = RsButton(
                    label: home.ctaPrimary.isEmpty ? 'Бренди' : home.ctaPrimary,
                    onPressed: () => context.go('/brands'),
                  );
                  final houseBtn = RsButton(
                    label: home.ctaSecondary.isEmpty ? 'Дім' : home.ctaSecondary,
                    variant: RsButtonVariant.secondary,
                    onPressed: () => context.go('/house'),
                  );
                  return Row(
                    children: [
                      Expanded(child: brandsBtn),
                      const SizedBox(width: AppSizes.s12),
                      Expanded(child: houseBtn),
                    ],
                  );
                },
              ),
            ],
          ),
        ),
        const SizedBox(height: AppSizes.s40),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSizes.padX),
          child: Text('ПАРТНЕРИ', style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
        ),
        const SizedBox(height: AppSizes.s12),
        SizedBox(
          height: 128,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: AppSizes.padX),
            itemCount: brands.length,
            separatorBuilder: (_, _) => const SizedBox(width: AppSizes.s12),
            itemBuilder: (context, index) {
              final brand = brands[index];
              return RsPartnerMark(
                brand: brand,
                onTap: () => context.go('/brands/${brand.id}'),
              );
            },
          ),
        ),
        const SizedBox(height: AppSizes.s40),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSizes.padX),
          child: Column(
            children: [
              const Divider(height: 1, color: AppColors.hairline),
              RsEditorialRow(label: 'Про дім', onTap: () => context.go('/house')),
              RsEditorialRow(label: 'Контакти', onTap: () => context.go('/more/contacts')),
              RsEditorialRow(label: 'Забронювати візит', onTap: () => context.go('/house/visit')),
            ],
          ),
        ),
      ],
    );
  }
}
