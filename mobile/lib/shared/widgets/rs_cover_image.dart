import 'package:flutter/material.dart';

/// Мережеве фото з fallback на asset (або градієнт).
class RsCoverImage extends StatelessWidget {
  const RsCoverImage({
    super.key,
    required this.imageUrl,
    required this.assetFallback,
    this.fit = BoxFit.cover,
  });

  final String imageUrl;
  final String assetFallback;
  final BoxFit fit;

  @override
  Widget build(BuildContext context) {
    if (imageUrl.isNotEmpty) {
      return Image.network(
        imageUrl,
        fit: fit,
        errorBuilder: (_, __, ___) => Image.asset(assetFallback, fit: fit),
        loadingBuilder: (context, child, progress) {
          if (progress == null) return child;
          return ColoredBox(
            color: const Color(0xFF1C1715),
            child: child,
          );
        },
      );
    }
    return Image.asset(assetFallback, fit: fit);
  }
}
