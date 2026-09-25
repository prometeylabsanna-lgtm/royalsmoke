import 'package:flutter/material.dart';

import 'app_colors.dart';

/// Типографіка прототипу. Fixel не має накреслення 650 — заголовки на SemiBold (600).
abstract final class AppTextStyles {
  static const String family = 'Fixel Display';

  static double _track(double size, double em) => size * em;

  static TextStyle get title => TextStyle(
        fontFamily: family,
        fontSize: 28,
        fontWeight: FontWeight.w600,
        height: 1.12,
        letterSpacing: _track(28, 0.26),
        color: AppColors.seashell,
      );

  static TextStyle get body => const TextStyle(
        fontFamily: family,
        fontSize: 15,
        fontWeight: FontWeight.w500,
        height: 1.5,
        color: AppColors.seashell,
      );

  static TextStyle get kicker => TextStyle(
        fontFamily: family,
        fontSize: 11,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: _track(11, 0.3),
        color: AppColors.textMuted,
      );

  static TextStyle get link => TextStyle(
        fontFamily: family,
        fontSize: 12,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: _track(12, 0.2),
        color: AppColors.textMuted,
        decoration: TextDecoration.underline,
        decorationColor: AppColors.gold,
      );

  static TextStyle get button => TextStyle(
        fontFamily: family,
        fontSize: 13,
        fontWeight: FontWeight.w600,
        height: 1.2,
        letterSpacing: _track(13, 0.22),
        color: AppColors.bark,
      );

  static TextStyle get hero => TextStyle(
        fontFamily: family,
        fontSize: 42,
        fontWeight: FontWeight.w600,
        height: 1.08,
        letterSpacing: _track(42, 0.24),
        color: AppColors.seashell,
      );

  static TextStyle get brandName => TextStyle(
        fontFamily: family,
        fontSize: 15,
        fontWeight: FontWeight.w600,
        height: 1.2,
        letterSpacing: _track(15, 0.06),
        color: AppColors.seashell,
      );

  static TextStyle get country => TextStyle(
        fontFamily: family,
        fontSize: 11,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: _track(11, 0.2),
        color: AppColors.textMuted,
      );

  static TextStyle get chip => TextStyle(
        fontFamily: family,
        fontSize: 12,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: _track(12, 0.14),
        color: AppColors.gold,
      );

  static TextStyle get back => TextStyle(
        fontFamily: family,
        fontSize: 12,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: _track(12, 0.18),
        color: AppColors.seashell,
      );

  static TextStyle get error => const TextStyle(
        fontFamily: family,
        fontSize: 13,
        fontWeight: FontWeight.w500,
        height: 1.4,
        color: AppColors.gold,
      );

  static TextStyle get tabLabel => TextStyle(
        fontFamily: family,
        fontSize: 10,
        fontWeight: FontWeight.w500,
        height: 1.2,
        letterSpacing: _track(10, 0.04),
        color: AppColors.textMuted,
      );
}
