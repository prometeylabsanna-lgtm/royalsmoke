import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/brands/data/partner_catalog.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_rows.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final heroHeight = (MediaQuery.sizeOf(context).height * 0.48).clamp(280.0, 430.0);
    return ListView(
      padding: const EdgeInsets.only(bottom: AppSizes.s24),
      children: [
        SizedBox(
          height: heroHeight,
          child: Stack(
            fit: StackFit.expand,
            children: [
              Image.asset(
                'assets/images/home/hero.jpg',
                fit: BoxFit.cover,
                alignment: Alignment.center,
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
              Text('ДІМ БРЕНДУ', style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
              const SizedBox(height: AppSizes.s16),
              Text('ROYAL\nSMOKE', style: AppTextStyles.hero),
              const SizedBox(height: AppSizes.s16),
              Text('Довідник дому бренду та партнерів', style: AppTextStyles.body),
              const SizedBox(height: AppSizes.s24),
              Builder(
                builder: (context) {
                  final brands = RsButton(label: 'Бренди', onPressed: () => context.go('/brands'));
                  final house = RsButton(
                    label: 'Про дім',
                    variant: RsButtonVariant.ghost,
                    onPressed: () => context.go('/house'),
                  );
                  if (MediaQuery.sizeOf(context).width < 360) {
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [brands, house],
                    );
                  }
                  return Row(children: [brands, const SizedBox(width: AppSizes.s8), house]);
                },
              ),
            ],
          ),
        ),
        const SizedBox(height: AppSizes.s56),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSizes.padX),
          child: Text('ПАРТНЕРИ', style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
        ),
        const SizedBox(height: AppSizes.s16),
        SizedBox(
          height: 110,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: AppSizes.padX),
            itemCount: PartnerCatalog.brands.length,
            separatorBuilder: (_, _) => const SizedBox(width: AppSizes.s12),
            itemBuilder: (context, index) {
              final brand = PartnerCatalog.brands[index];
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
