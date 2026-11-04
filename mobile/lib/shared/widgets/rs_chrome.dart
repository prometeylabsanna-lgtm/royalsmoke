import 'package:flutter/material.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import 'rs_insets.dart';

enum RsTab { home, house, visit, contacts, more }

class RsPageHeading extends StatelessWidget {
  const RsPageHeading({
    super.key,
    required this.kicker,
    required this.title,
    this.subtitle,
    this.compactTitle = false,
    this.titleTrackingEm,
  });

  final String kicker;
  final String title;
  final String? subtitle;

  /// Менший letter-spacing і перенос лише по словах (для довгих юр. заголовків).
  final bool compactTitle;

  /// Трекінг заголовка в em. null лишає стиль title.
  final double? titleTrackingEm;

  @override
  Widget build(BuildContext context) {
    var titleStyle = compactTitle
        ? AppTextStyles.title.copyWith(
            fontSize: 26,
            letterSpacing: 26 * 0.08,
            height: 1.15,
          )
        : AppTextStyles.title;
    final tracking = titleTrackingEm;
    if (tracking != null) {
      final size = titleStyle.fontSize ?? 28;
      titleStyle = titleStyle.copyWith(letterSpacing: size * tracking);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          kicker.toUpperCase(),
          style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.32),
        ),
        const SizedBox(height: 10),
        if (compactTitle)
          _WordSafeTitle(text: title.toUpperCase(), style: titleStyle)
        else
          Text(title.toUpperCase(), style: titleStyle),
        if (subtitle != null) ...[
          const SizedBox(height: 4),
          Text(subtitle!, style: AppTextStyles.body),
        ],
      ],
    );
  }
}

/// Заголовок без розриву слова посередині: кожне слово — окремий рядок із scaleDown.
class _WordSafeTitle extends StatelessWidget {
  const _WordSafeTitle({required this.text, required this.style});

  final String text;
  final TextStyle style;

  @override
  Widget build(BuildContext context) {
    final words = text
        .trim()
        .split(RegExp(r'\s+'))
        .where((w) => w.isNotEmpty)
        .toList();
    if (words.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (final word in words)
          FittedBox(
            fit: BoxFit.scaleDown,
            alignment: Alignment.centerLeft,
            child: Text(word, maxLines: 1, softWrap: false, style: style),
          ),
      ],
    );
  }
}

class RsBackBar extends StatelessWidget {
  const RsBackBar({
    super.key,
    required this.label,
    this.onPressed,
    this.trailing,
  });

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
        AppLocalizations.of(context).ageBadge,
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
      child: const CustomPaint(painter: _SealMarkPainter()),
    );
  }
}

class RsTabBar extends StatelessWidget {
  const RsTabBar({super.key, required this.current, required this.onChanged});

  final RsTab current;
  final ValueChanged<RsTab> onChanged;

  List<(RsTab, String)> _items(AppLocalizations l10n) {
    return [
      (RsTab.home, l10n.tabHome),
      (RsTab.house, l10n.houseTab),
      (RsTab.visit, l10n.visitTitle),
      (RsTab.contacts, l10n.contacts),
      (RsTab.more, l10n.moreTitle),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final items = _items(AppLocalizations.of(context));
    final edges = rsSafeEdges(context, top: false, bottom: true);
    return DecoratedBox(
      decoration: const BoxDecoration(color: AppColors.canvas),
      child: Padding(
        padding: EdgeInsets.only(
          left: edges.left,
          right: edges.right,
          bottom: edges.bottom,
        ),
        child: Padding(
          padding: const EdgeInsets.only(top: 6),
          child: SizedBox(
            height: 48,
            child: Row(
              children: [
                for (final item in items)
                  Expanded(
                    child: Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: () => onChanged(item.$1),
                        child: SizedBox(
                          height: 48,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _TabGlyph(
                                tab: item.$1,
                                active: item.$1 == current,
                              ),
                              const SizedBox(height: 4),
                              Padding(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 2,
                                ),
                                child: FittedBox(
                                  fit: BoxFit.scaleDown,
                                  child: Text(
                                    item.$2,
                                    maxLines: 1,
                                    softWrap: false,
                                    style: AppTextStyles.tabLabel.copyWith(
                                      color: item.$1 == current
                                          ? AppColors.gold
                                          : AppColors.tabInactive,
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
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
    final color = active ? AppColors.gold : AppColors.tabInactive;
    return switch (tab) {
      RsTab.home => Icon(
        active ? Icons.home : Icons.home_outlined,
        size: AppSizes.tabIcon,
        color: color,
      ),
      RsTab.house => Icon(
        active ? Icons.room_service : Icons.room_service_outlined,
        size: AppSizes.tabIcon,
        color: color,
      ),
      _ => CustomPaint(
        size: const Size(AppSizes.tabIcon, AppSizes.tabIcon),
        painter: _TabPainter(tab: tab, color: color),
      ),
    };
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
      case RsTab.house:
        return;
      case RsTab.visit:
        path
          ..addRRect(
            RRect.fromRectAndRadius(
              const Rect.fromLTWH(4, 5, 16, 14),
              const Radius.circular(2),
            ),
          )
          ..moveTo(4, 9)
          ..lineTo(20, 9)
          ..moveTo(8, 3)
          ..lineTo(8, 7)
          ..moveTo(16, 3)
          ..lineTo(16, 7);
      case RsTab.contacts:
        canvas.drawCircle(const Offset(12, 7.5), 3.2, paint);
        path
          ..moveTo(5.5, 19)
          ..quadraticBezierTo(12, 13.2, 18.5, 19);
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

class _SealMarkPainter extends CustomPainter {
  const _SealMarkPainter();

  @override
  void paint(Canvas canvas, Size size) {
    final side = size.shortestSide;
    final center = Offset(size.width / 2, size.height / 2);
    final ring = Paint()
      ..color = AppColors.gold
      ..style = PaintingStyle.stroke
      ..strokeWidth = side * 0.045;
    canvas.drawCircle(center, side * 0.40, ring);

    final inner = Paint()
      ..color = AppColors.gold
      ..style = PaintingStyle.stroke
      ..strokeWidth = side * 0.018;
    canvas.drawCircle(center, side * 0.30, inner);

    final diamond = Path()
      ..moveTo(center.dx, center.dy - side * 0.11)
      ..lineTo(center.dx + side * 0.08, center.dy)
      ..lineTo(center.dx, center.dy + side * 0.11)
      ..lineTo(center.dx - side * 0.08, center.dy)
      ..close();
    canvas.drawPath(diamond, Paint()..color = AppColors.gold);
  }

  @override
  bool shouldRepaint(covariant _SealMarkPainter oldDelegate) => false;
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
