import 'package:flutter/foundation.dart';

/// Повільний ken-burns спільного фону.
///
/// Масштаб лишається в діапазоні 2–4% понад 1.0. Зміщення не виходить
/// за запас масштабу, тож картинка завжди перекриває ширину екрана.
abstract final class BackdropMotion {
  static const Duration kenBurnsDuration = Duration(seconds: 24);
  static const Duration glowDuration = Duration(seconds: 8);
  static const double glowPeakOpacity = 0.15;
  static const double imagePixelWidth = 1152;
  static const double imagePixelHeight = 2048;

  static double get imageAspect => imagePixelHeight / imagePixelWidth;

  static BackdropFrame at({
    required double t,
    required double width,
    required double imageHeight,
  }) {
    final clamped = t.isNaN ? 0.0 : t.clamp(0.0, 1.0);
    final scale = 1.02 + 0.02 * clamped;
    final slack = width * (scale - 1) / 2;
    final dx = slack * 0.72 * (clamped * 2 - 1);
    final dy = -imageHeight * 0.02 * clamped;
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
