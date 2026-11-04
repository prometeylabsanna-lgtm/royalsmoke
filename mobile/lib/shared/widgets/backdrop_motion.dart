import 'package:flutter/foundation.dart';

/// Повільний ken-burns спільного фону.
///
/// Півцикл 6 с; `repeat(reverse: true)` дає повний цикл 12 с.
/// Масштаб 1.0…1.12. Горизонтальний зсув лишається в запасі масштабу,
/// тож краї кадру не відкриваються.
abstract final class BackdropMotion {
  static const Duration kenBurnsDuration = Duration(seconds: 6);
  static const Duration glowDuration = Duration(seconds: 6);
  static const double glowPeakOpacity = 0.35;
  static const double imagePixelWidth = 1152;
  static const double imagePixelHeight = 2048;

  static double get imageAspect => imagePixelHeight / imagePixelWidth;

  static BackdropFrame at({
    required double t,
    required double width,
    required double imageHeight,
  }) {
    final clamped = t.isNaN ? 0.0 : t.clamp(0.0, 1.0);
    final scale = 1.0 + 0.12 * clamped;
    final slack = width * (scale - 1) / 2;
    final dx = slack * 0.6 * (2 * clamped - 1);
    final dy = -imageHeight * 0.03 * clamped;
    return BackdropFrame(scale: scale, dx: dx, dy: dy);
  }
}

@immutable
class BackdropFrame {
  const BackdropFrame({
    required this.scale,
    required this.dx,
    required this.dy,
  });

  final double scale;
  final double dx;
  final double dy;
}
