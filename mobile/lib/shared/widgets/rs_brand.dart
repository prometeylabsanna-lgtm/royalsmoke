import 'package:flutter/material.dart';

import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../features/brands/domain/partner_brand.dart';

/// Назва бренду: перенос лише по словах, без одиночної літери на рядку.
class RsBrandTitle extends StatelessWidget {
  const RsBrandTitle({
    super.key,
    required this.name,
    required this.style,
    this.textAlign = TextAlign.center,
    this.maxLines = 3,
  });

  final String name;
  final TextStyle style;
  final TextAlign textAlign;
  final int maxLines;

  @override
  Widget build(BuildContext context) {
    final words = name
        .trim()
        .toUpperCase()
        .split(RegExp(r'\s+'))
        .where((w) => w.isNotEmpty)
        .toList();
    if (words.isEmpty) return const SizedBox.shrink();

    // Кожне слово — окремий рядок, масштаб вниз якщо не вміщається.
    // Ніколи не рвемо слово посередині і не лишаємо одну літеру.
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: textAlign == TextAlign.left
          ? CrossAxisAlignment.start
          : textAlign == TextAlign.right
              ? CrossAxisAlignment.end
              : CrossAxisAlignment.center,
      children: [
        for (final word in words.take(maxLines))
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              word,
              maxLines: 1,
              softWrap: false,
              textAlign: textAlign,
              style: style,
            ),
          ),
      ],
    );
  }
}

class RsBrandCell extends StatelessWidget {
  const RsBrandCell({super.key, required this.brand, this.onTap});

  final PartnerBrand brand;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(AppSizes.radiusSearch),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  DecoratedBox(decoration: BoxDecoration(gradient: brand.gradient)),
                  Image.asset(brand.imageAsset, fit: BoxFit.cover),
                  const DecoratedBox(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [Colors.transparent, Color(0x66100D0C)],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 10),
          RsBrandTitle(
            name: brand.name,
            textAlign: TextAlign.left,
            style: AppTextStyles.brandName.copyWith(
              fontSize: 15,
              letterSpacing: 15 * 0.06,
              height: 1.15,
            ),
          ),
        ],
      ),
    );
  }
}

class RsPartnerMark extends StatelessWidget {
  const RsPartnerMark({super.key, required this.brand, this.onTap});

  final PartnerBrand brand;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: SizedBox(
        width: 96,
        child: Column(
          children: [
            Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: const Color(0x38FCF2EE)),
              ),
              child: ClipOval(
                child: Image.asset(brand.imageAsset, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(height: 10),
            RsBrandTitle(
              name: brand.shortName,
              style: AppTextStyles.country.copyWith(
                letterSpacing: 11 * 0.12,
                height: 1.2,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class RsOfflineBrandRow extends StatelessWidget {
  const RsOfflineBrandRow({super.key, required this.brand, this.onTap});

  final PartnerBrand brand;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: AppColors.hairline)),
        ),
        child: Row(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(AppSizes.radiusMd),
              child: SizedBox(
                width: 52,
                height: 52,
                child: Image.asset(brand.imageAsset, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  RsBrandTitle(
                    name: brand.name,
                    textAlign: TextAlign.left,
                    style: AppTextStyles.brandName.copyWith(letterSpacing: 15 * 0.04),
                  ),
                  const SizedBox(height: 2),
                  Text(brand.country.toUpperCase(), style: AppTextStyles.country),
                ],
              ),
            ),
            Text(
              'ЗБЕРЕЖЕНО',
              style: AppTextStyles.tabLabel.copyWith(letterSpacing: 10 * 0.18),
            ),
          ],
        ),
      ),
    );
  }
}

class RsMonogram extends StatelessWidget {
  const RsMonogram({
    super.key,
    required this.text,
    required this.size,
    required this.fontSize,
    this.borderColor = const Color(0x59FCF2EE),
  });

  final String text;
  final double size;
  final double fontSize;
  final Color borderColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: Border.all(color: borderColor),
        color: AppColors.bark.withValues(alpha: 0.28),
      ),
      child: Padding(
        padding: EdgeInsets.only(left: fontSize * 0.12),
        child: Text(
          text,
          style: TextStyle(
            fontFamily: AppTextStyles.family,
            fontSize: fontSize,
            fontWeight: FontWeight.w600,
            letterSpacing: fontSize * 0.12,
            color: AppColors.seashell,
          ),
        ),
      ),
    );
  }
}
