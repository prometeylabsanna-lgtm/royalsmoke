import 'package:flutter/material.dart';

import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';

class RsTextField extends StatelessWidget {
  const RsTextField({
    super.key,
    this.label,
    this.hint,
    this.controller,
    this.errorText,
    this.prefix,
    this.keyboardType,
    this.maxLines = 1,
    this.onChanged,
    this.onClear,
  });

  final String? label;
  final String? hint;
  final TextEditingController? controller;
  final String? errorText;
  final Widget? prefix;
  final TextInputType? keyboardType;
  final int maxLines;
  final ValueChanged<String>? onChanged;
  final VoidCallback? onClear;

  @override
  Widget build(BuildContext context) {
    final hasError = errorText != null && errorText!.isNotEmpty;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (label != null) ...[
          Text(label!.toUpperCase(), style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.24)),
          const SizedBox(height: AppSizes.s8),
        ],
        TextField(
          controller: controller,
          keyboardType: keyboardType,
          maxLines: maxLines,
          onChanged: onChanged,
          cursorColor: AppColors.gold,
          style: AppTextStyles.body,
          decoration: InputDecoration(
            hintText: hint,
            hintStyle: AppTextStyles.body.copyWith(color: AppColors.textPlaceholder),
            prefixIcon: prefix == null
                ? null
                : Padding(
                    padding: const EdgeInsets.only(left: 16, right: 10),
                    child: prefix,
                  ),
            prefixIconConstraints: const BoxConstraints(minWidth: 18, minHeight: 18),
            suffixIcon: onClear == null
                ? null
                : IconButton(
                    onPressed: onClear,
                    icon: const _ClearMark(),
                  ),
            filled: true,
            fillColor: AppColors.slot,
            contentPadding: EdgeInsets.symmetric(
              horizontal: 16,
              vertical: maxLines > 1 ? 14 : 0,
            ),
            constraints: maxLines == 1
                ? const BoxConstraints(minHeight: AppSizes.searchHeight)
                : null,
            enabledBorder: _border(hasError ? AppColors.gold : Colors.transparent),
            focusedBorder: _border(hasError ? AppColors.gold : AppColors.goldFocus),
            errorBorder: _border(AppColors.gold),
            focusedErrorBorder: _border(AppColors.gold),
          ),
        ),
        if (hasError) ...[
          const SizedBox(height: AppSizes.s8),
          Text(errorText!, style: AppTextStyles.error),
        ],
      ],
    );
  }

  OutlineInputBorder _border(Color color) {
    return OutlineInputBorder(
      borderRadius: BorderRadius.circular(AppSizes.radiusSearch),
      borderSide: BorderSide(color: color),
    );
  }
}

class _ClearMark extends StatelessWidget {
  const _ClearMark();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 20,
      height: 20,
      alignment: Alignment.center,
      decoration: const BoxDecoration(
        color: Color(0x2EFCF2EE),
        shape: BoxShape.circle,
      ),
      child: CustomPaint(
        size: const Size(8, 8),
        painter: _CrossPainter(),
      ),
    );
  }
}

class _CrossPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.bark
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;
    canvas.drawLine(Offset.zero, Offset(size.width, size.height), paint);
    canvas.drawLine(Offset(size.width, 0), Offset(0, size.height), paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
