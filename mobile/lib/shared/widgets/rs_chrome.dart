import 'package:flutter/material.dart';

import '../../core/constants/app_copy.dart';
import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';

enum RsTab { home, brands, house, offline, more }

class RsPageHeading extends StatelessWidget {
  const RsPageHeading({super.key, required this.kicker, required this.title, this.subtitle});

  final String kicker;
  final String title;
  final String? subtitle;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(kicker.toUpperCase(), style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32)),
        const SizedBox(height: 10),
        Text(title.toUpperCase(), style: AppTextStyles.title),
        if (subtitle != null) ...[
          const SizedBox(height: 4),
          Text(subtitle!, style: AppTextStyles.body),
        ],
      ],
    );
  }
}

class RsBackBar extends StatelessWidget {
  const RsBackBar({super.key, required this.label, this.onPressed, this.trailing});

  final String label;
  final VoidCallback? onPressed;
  final Widget? trailing;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: AppSizes.tap,
      child: Row(
        children: [
          InkWell(
            onTap: onPressed,
            child: Row(
              children: [
                CustomPaint(size: const Size(16, 16), painter: _BackPainter()),
                const SizedBox(width: 6),
                Text(label.toUpperCase(), style: AppTextStyles.back),
              ],
            ),
          ),
          const Spacer(),
          if (trailing != null) trailing!,
        ],
      ),
    );
  }
}

class RsAgeBadge extends StatelessWidget {
  const RsAgeBadge({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: const Color(0x33FCF2EE)),
      ),
      child: Text(
        AppCopy.ageBadge,
        style: AppTextStyles.tabLabel.copyWith(letterSpacing: 10 * 0.2),
      ),
    );
  }
}

class RsSeal extends StatelessWidget {
  const RsSeal({super.key, this.size = 120});

  final double size;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: size,
      height: size,
      child: ClipOval(
        child: Image.asset(
          'assets/images/branding/seal.jpg',
          fit: BoxFit.cover,
          errorBuilder: (_, _, _) => Container(
            color: AppColors.coffee,
            alignment: Alignment.center,
            child: Text(
              'RS',
              style: TextStyle(
                fontFamily: AppTextStyles.family,
                fontSize: size * 0.2,
                fontWeight: FontWeight.w600,
                color: AppColors.gold,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class RsEmptySearch extends StatelessWidget {
  const RsEmptySearch({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 64,
          height: 64,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(color: AppColors.gold),
          ),
          child: Container(
            width: 54,
            height: 54,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: AppColors.gold.withValues(alpha: 0.35)),
            ),
            child: Text(
              'RS',
              style: AppTextStyles.brandName.copyWith(
                fontSize: 14,
                letterSpacing: 14 * 0.14,
                color: AppColors.gold,
              ),
            ),
          ),
        ),
        const SizedBox(height: AppSizes.s16),
        Text('Нічого не знайдено', style: AppTextStyles.body.copyWith(fontSize: 17, fontWeight: FontWeight.w600)),
        const SizedBox(height: AppSizes.s8),
        Text('Спробуйте іншу назву', style: AppTextStyles.body.copyWith(fontSize: 14, color: AppColors.textMuted)),
      ],
    );
  }
}

class RsOfflineChip extends StatelessWidget {
  const RsOfflineChip({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 28,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppSizes.radiusChip),
        border: Border.all(color: const Color(0x33FCF2EE)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 6,
            height: 6,
            decoration: const BoxDecoration(color: AppColors.gold, shape: BoxShape.circle),
          ),
          const SizedBox(width: AppSizes.s8),
          Text(
            'ОФЛАЙН-РЕЖИМ',
            style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.16, color: AppColors.seashell),
          ),
        ],
      ),
    );
  }
}

class RsTabBar extends StatelessWidget {
  const RsTabBar({super.key, required this.current, required this.onChanged});

  final RsTab current;
  final ValueChanged<RsTab> onChanged;

  static const _items = <(RsTab, String)>[
    (RsTab.home, 'Головна'),
    (RsTab.brands, 'Бренди'),
    (RsTab.house, 'Дім'),
    (RsTab.offline, 'Офлайн'),
    (RsTab.more, 'Ще'),
  ];

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: const BoxDecoration(
        color: AppColors.coffee,
        border: Border(top: BorderSide(color: Color(0x1AFCF2EE))),
      ),
      child: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.only(top: 6),
          child: SizedBox(
            height: 48,
            child: Row(
              children: [
                for (final item in _items)
                  Expanded(
                    child: InkWell(
                      onTap: () => onChanged(item.$1),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          _TabGlyph(tab: item.$1, active: item.$1 == current),
                          const SizedBox(height: 4),
                          Text(
                            item.$2,
                            style: AppTextStyles.tabLabel.copyWith(
                              color: item.$1 == current ? AppColors.gold : AppColors.tabInactive,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _TabGlyph extends StatelessWidget {
  const _TabGlyph({required this.tab, required this.active});

  final RsTab tab;
  final bool active;

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: const Size(AppSizes.tabIcon, AppSizes.tabIcon),
      painter: _TabPainter(tab: tab, color: active ? AppColors.gold : AppColors.tabInactive),
    );
  }
}

class _TabPainter extends CustomPainter {
  _TabPainter({required this.tab, required this.color});

  final RsTab tab;
  final Color color;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4
      ..strokeJoin = StrokeJoin.round
      ..strokeCap = StrokeCap.round;
    final path = Path();
    switch (tab) {
      case RsTab.home:
        path
          ..moveTo(4, 11)
          ..lineTo(12, 5)
          ..lineTo(20, 11)
          ..lineTo(20, 20)
          ..lineTo(15, 20)
          ..lineTo(15, 15)
          ..lineTo(9, 15)
          ..lineTo(9, 20)
          ..lineTo(4, 20)
          ..close();
      case RsTab.brands:
        for (final origin in const [Offset(4, 4), Offset(13, 4), Offset(4, 13), Offset(13, 13)]) {
          path.addRect(Rect.fromLTWH(origin.dx, origin.dy, 7, 7));
        }
      case RsTab.house:
        path
          ..moveTo(3.5, 9)
          ..lineTo(12, 4)
          ..lineTo(20.5, 9);
        for (final x in const [6.0, 10.0, 14.0, 18.0]) {
          path
            ..moveTo(x, 10)
            ..lineTo(x, 18);
        }
        path
          ..moveTo(4, 20.5)
          ..lineTo(20, 20.5);
      case RsTab.offline:
        path
          ..addRect(const Rect.fromLTWH(4, 8, 16, 12))
          ..addRect(const Rect.fromLTWH(3, 4, 18, 4))
          ..moveTo(10, 12)
          ..lineTo(14, 12);
      case RsTab.more:
        canvas.drawCircle(const Offset(6, 12), 1.2, Paint()..color = color);
        canvas.drawCircle(const Offset(12, 12), 1.2, Paint()..color = color);
        canvas.drawCircle(const Offset(18, 12), 1.2, Paint()..color = color);
        return;
    }
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant _TabPainter oldDelegate) =>
      oldDelegate.tab != tab || oldDelegate.color != color;
}

class _BackPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.seashell
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    final path = Path()
      ..moveTo(10, 3)
      ..lineTo(5, 8)
      ..lineTo(10, 13);
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
