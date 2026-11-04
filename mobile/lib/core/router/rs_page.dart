import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Сторінка без власного полотна: крізь неї видно спільний фон.
/// Вхід і вихід — короткий fade, тож тексти не лежать один на одному.
CustomTransitionPage<void> rsOpaquePage({
  required LocalKey key,
  required Widget child,
  String? name,
}) {
  return CustomTransitionPage<void>(
    key: key,
    name: name,
    opaque: true,
    barrierColor: Colors.transparent,
    transitionDuration: const Duration(milliseconds: 180),
    reverseTransitionDuration: const Duration(milliseconds: 140),
    child: child,
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      final fadeIn = CurvedAnimation(
        parent: animation,
        curve: Curves.easeOutCubic,
      );
      final fadeOut = Tween<double>(begin: 1, end: 0).animate(
        CurvedAnimation(parent: secondaryAnimation, curve: Curves.easeOutCubic),
      );
      return FadeTransition(
        opacity: fadeIn,
        child: FadeTransition(opacity: fadeOut, child: child),
      );
    },
  );
}
