import 'package:flutter/material.dart';

import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';

class RsChip extends StatelessWidget {
  const RsChip({
    super.key,
    required this.label,
    this.selected = false,
    this.onTap,
  });

  final String label;
  final bool selected;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final color = selected ? AppColors.gold : AppColors.textMuted;
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSizes.radiusChip),
        child: Container(
          height: AppSizes.chipHeight,
          padding: const EdgeInsets.symmetric(horizontal: 14),
          alignment: Alignment.center,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(AppSizes.radiusChip),
            border: Border.all(color: selected ? AppColors.gold : AppColors.hairline),
          ),
          child: Text(label.toUpperCase(), style: AppTextStyles.chip.copyWith(color: color)),
        ),
      ),
    );
  }
}

class RsEditorialRow extends StatelessWidget {
  const RsEditorialRow({
    super.key,
    required this.label,
    this.onTap,
    this.trailing,
    this.leading,
  });

  final String label;
  final VoidCallback? onTap;
  final Widget? trailing;
  final Widget? leading;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        constraints: const BoxConstraints(minHeight: 60),
        padding: const EdgeInsets.symmetric(vertical: 8),
        decoration: const BoxDecoration(
          border: Border(bottom: BorderSide(color: AppColors.hairline)),
        ),
        child: Row(
          children: [
            if (leading != null) ...[
              leading!,
              const SizedBox(width: AppSizes.s12),
            ],
            Expanded(child: Text(label, style: AppTextStyles.body)),
            if (trailing != null) trailing!,
            const SizedBox(width: AppSizes.s8),
            const _Chevron(),
          ],
        ),
      ),
    );
  }
}

class RsFactRow extends StatelessWidget {
  const RsFactRow({super.key, required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final narrow = MediaQuery.sizeOf(context).width < 360;
    final labelStyle = AppTextStyles.body.copyWith(fontSize: 14, color: AppColors.textMuted, height: 1.4);
    final valueStyle = AppTextStyles.body.copyWith(fontSize: 14, height: 1.4);
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: AppColors.hairline)),
      ),
      child: narrow
          ? Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: labelStyle),
                const SizedBox(height: 4),
                Text(value, style: valueStyle),
              ],
            )
          : Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(width: 128, child: Text(label, style: labelStyle)),
                const SizedBox(width: AppSizes.s12),
                Expanded(child: Text(value, style: valueStyle)),
              ],
            ),
    );
  }
}

class RsLineRow extends StatelessWidget {
  const RsLineRow({super.key, required this.index, required this.title});

  final int index;
  final String title;

  @override
  Widget build(BuildContext context) {
    final number = index.toString().padLeft(2, '0');
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: AppColors.hairline)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.baseline,
        textBaseline: TextBaseline.alphabetic,
        children: [
          SizedBox(
            width: 20,
            child: Text(number, style: AppTextStyles.kicker.copyWith(color: AppColors.gold, letterSpacing: 1.1)),
          ),
          const SizedBox(width: AppSizes.s16),
          Expanded(
            child: Text(title, style: AppTextStyles.body.copyWith(letterSpacing: 15 * 0.02)),
          ),
        ],
      ),
    );
  }
}

class _Chevron extends StatelessWidget {
  const _Chevron();

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: const Size(16, 16),
      painter: _ChevronPainter(),
    );
  }
}

class _ChevronPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.gold
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    final path = Path()
      ..moveTo(6, 3)
      ..lineTo(11, 8)
      ..lineTo(6, 13);
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
