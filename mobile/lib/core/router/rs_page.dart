import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../theme/app_colors.dart';

/// Непрозора сторінка з коротким fade — без просвічування попереднього тексту.
CustomTransitionPage<void> rsOpaquePage({
  required LocalKey key,
  required Widget child,
  String? name,
}) {
  return CustomTransitionPage<void>(
    key: key,
    name: name,
    opaque: true,
    barrierColor: AppColors.bark,
    transitionDuration: const Duration(milliseconds: 180),
    reverseTransitionDuration: const Duration(milliseconds: 140),
    child: ColoredBox(color: AppColors.bark, child: child),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      final fade = CurvedAnimation(parent: animation, curve: Curves.easeOutCubic);
      return FadeTransition(opacity: fade, child: child);
    },
  );
}
