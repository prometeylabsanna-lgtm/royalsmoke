import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app_colors.dart';
import 'app_text_styles.dart';

abstract final class AppTheme {
  static const SystemUiOverlayStyle overlay = SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
    statusBarBrightness: Brightness.dark,
    systemNavigationBarColor: AppColors.canvas,
    systemNavigationBarDividerColor: AppColors.canvas,
    systemNavigationBarIconBrightness: Brightness.light,
    systemNavigationBarContrastEnforced: false,
    systemStatusBarContrastEnforced: false,
  );

  static ThemeData get dark {
    const scheme = ColorScheme.dark(
      surface: AppColors.canvas,
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
      canvasColor: AppColors.canvas,
      scaffoldBackgroundColor: AppColors.canvas,
      pageTransitionsTheme: const PageTransitionsTheme(
        builders: {
          TargetPlatform.iOS: FadeUpwardsPageTransitionsBuilder(),
          TargetPlatform.macOS: FadeUpwardsPageTransitionsBuilder(),
          TargetPlatform.android: FadeUpwardsPageTransitionsBuilder(),
        },
      ),
      colorScheme: scheme,
      textTheme: TextTheme(
        headlineMedium: AppTextStyles.title,
        bodyMedium: AppTextStyles.body,
        labelSmall: AppTextStyles.kicker,
        labelLarge: AppTextStyles.button,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        foregroundColor: AppColors.seashell,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: true,
        systemOverlayStyle: overlay,
      ),
      dividerTheme: const DividerThemeData(
        color: AppColors.hairline,
        thickness: 1,
        space: 1,
      ),
    );
  }
}
