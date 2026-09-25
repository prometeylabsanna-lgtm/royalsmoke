import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app_colors.dart';
import 'app_text_styles.dart';

abstract final class AppTheme {
  static ThemeData get dark {
    const scheme = ColorScheme.dark(
      surface: AppColors.bark,
      primary: AppColors.gold,
      onPrimary: AppColors.bark,
      secondary: AppColors.gold,
      onSecondary: AppColors.bark,
      onSurface: AppColors.seashell,
      outline: AppColors.hairline,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      fontFamily: AppTextStyles.family,
      scaffoldBackgroundColor: AppColors.bark,
      colorScheme: scheme,
      textTheme: TextTheme(
        headlineMedium: AppTextStyles.title,
        bodyMedium: AppTextStyles.body,
        labelSmall: AppTextStyles.kicker,
        labelLarge: AppTextStyles.button,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.bark,
        foregroundColor: AppColors.seashell,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: true,
        systemOverlayStyle: SystemUiOverlayStyle(
          statusBarColor: AppColors.bark,
          statusBarIconBrightness: Brightness.light,
          statusBarBrightness: Brightness.dark,
        ),
      ),
      dividerTheme: const DividerThemeData(
        color: AppColors.hairline,
        thickness: 1,
        space: 1,
      ),
    );
  }
}
