import 'package:flutter/material.dart';

import '../../core/theme/app_text_styles.dart';
import '../../features/brands/domain/partner_brand.dart';

/// Фон-водяний знак як на головній сайту: повтор назви бренду, золоті акценти.
class RsBrandLetterPattern extends StatelessWidget {
  const RsBrandLetterPattern({
    super.key,
    required this.word,
    required this.panel,
    this.fontSize = 18,
    this.rowCount = 16,
    this.extendLower = false,
  });

  final String word;
  final BrandPanel panel;
  final double fontSize;
  final int rowCount;
  /// М’якший fade вниз — патерн видно нижче по картці.
  final bool extendLower;

  String get _token {
    final cleaned = word.replaceAll(RegExp(r'\s+'), '').toUpperCase();
    return cleaned.isEmpty ? 'RS' : cleaned;
  }

  Color get _ink => switch (panel) {
        BrandPanel.amber => const Color(0x38D2B48C),
        BrandPanel.burgundy => const Color(0x33C4A0A8),
        BrandPanel.green => const Color(0x33A8C4B0),
        BrandPanel.brown => const Color(0x33C4B4A0),
      };

  static const Color _gold = Color(0x94C99A44);

  @override
  Widget build(BuildContext context) {
    final token = _token;
    final repeats = (28 / token.length).ceil().clamp(4, 14);
    final line = List.filled(repeats, token).join();

    final mask = extendLower
        ? const LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color(0xF2000000),
              Color(0xD9000000),
              Color(0xB3000000),
              Color(0x80000000),
              Color(0x4D000000),
              Color(0x1A000000),
            ],
            stops: [0, 0.28, 0.5, 0.7, 0.88, 1],
          )
        : const LinearGradient(
            begin: Alignment(-0.8, -0.6),
            end: Alignment(0.8, 0.6),
            colors: [
              Color(0xF2000000),
              Color(0x8C000000),
              Color(0x1F000000),
              Color(0x0A000000),
              Color(0x0A000000),
              Color(0x1F000000),
              Color(0x8C000000),
              Color(0xF2000000),
            ],
            stops: [0, 0.16, 0.36, 0.48, 0.52, 0.64, 0.84, 1],
          );

    return IgnorePointer(
      child: ShaderMask(
        blendMode: BlendMode.dstIn,
        shaderCallback: (bounds) => mask.createShader(bounds),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            for (var r = 0; r < rowCount; r++)
              Transform.translate(
                offset: Offset(r.isEven ? -fontSize * 1.35 : fontSize * 0.15, 0),
                child: _PatternRow(
                  line: line,
                  tokenLength: token.length,
                  rowIndex: r,
                  fontSize: fontSize,
                  ink: _ink,
                  gold: _gold,
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class _PatternRow extends StatelessWidget {
  const _PatternRow({
    required this.line,
    required this.tokenLength,
    required this.rowIndex,
    required this.fontSize,
    required this.ink,
    required this.gold,
  });

  final String line;
  final int tokenLength;
  final int rowIndex;
  final double fontSize;
  final Color ink;
  final Color gold;

  bool _isGold(int index) {
    // Як на сайті: кілька золотих літер зі зсувом по рядках.
    final accentInWord = (rowIndex * 2 + 1) % tokenLength;
    final phase = (rowIndex * 7) % tokenLength;
    return index % tokenLength == accentInWord || index % tokenLength == phase;
  }

  @override
  Widget build(BuildContext context) {
    return Text.rich(
      TextSpan(
        children: [
          for (var i = 0; i < line.length; i++)
            TextSpan(
              text: line[i],
              style: TextStyle(color: _isGold(i) ? gold : ink),
            ),
        ],
      ),
      maxLines: 1,
      softWrap: false,
      overflow: TextOverflow.visible,
      style: TextStyle(
        fontFamily: AppTextStyles.family,
        fontWeight: FontWeight.w600,
        fontSize: fontSize,
        height: 1.22,
        letterSpacing: fontSize * 0.18,
      ),
    );
  }
}

/// Панель бренду: градієнт + літерний патерн (+ опційний монограм у центрі).
class RsBrandLetterPanel extends StatelessWidget {
  const RsBrandLetterPanel({
    super.key,
    required this.brand,
    this.child,
    this.borderRadius,
    this.fontSize = 18,
    this.patternWord,
    this.rowCount = 14,
    this.extendLower = false,
  });

  final PartnerBrand brand;
  final Widget? child;
  final BorderRadius? borderRadius;
  final double fontSize;
  /// Якщо null — водяний знак з shortName бренду.
  final String? patternWord;
  final int rowCount;
  final bool extendLower;

  @override
  Widget build(BuildContext context) {
    final patternHeight = extendLower ? 900.0 : 600.0;
    return ClipRect(
      child: Stack(
        fit: StackFit.expand,
        clipBehavior: Clip.hardEdge,
        children: [
          DecoratedBox(decoration: BoxDecoration(gradient: brand.gradient)),
          Positioned.fill(
            child: ClipRect(
              child: OverflowBox(
                alignment: extendLower ? Alignment.topLeft : Alignment.centerLeft,
                maxWidth: 800,
                maxHeight: patternHeight,
                child: RsBrandLetterPattern(
                  word: patternWord ?? brand.shortName,
                  panel: brand.panel,
                  fontSize: fontSize,
                  rowCount: rowCount,
                  extendLower: extendLower,
                ),
              ),
            ),
          ),
          if (child != null) child!,
        ],
      ),
    );
  }
}
