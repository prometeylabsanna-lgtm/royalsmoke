import 'package:flutter/material.dart';

/// Токени з прототипу Royal Smoke (фрейм 00) і сайту.
abstract final class AppColors {
  static const Color bark = Color(0xFF100D0C);
  static const Color barkLight = Color(0xFF181412);
  static const Color coffee = Color(0xFF1C1715);
  static const Color slot = Color(0xFF322A26);
  static const Color seashell = Color(0xFFFCF2EE);
  static const Color gold = Color(0xFFC99A44);

  /// Натиснутий акцент з токенів сайту (`--rs-gold-hover`).
  static const Color goldHover = Color(0xFFD8AC5C);

  /// seashell @ 62% — неактивний таб
  static const Color tabInactive = Color(0x9EFCF2EE);

  /// seashell @ 40% — placeholder
  static const Color textPlaceholder = Color(0x66FCF2EE);

  /// gold @ 50% — рамка фокусу
  static const Color goldFocus = Color(0x80C99A44);

  /// seashell @ 60%
  static const Color textMuted = Color(0x99FCF2EE);

  /// seashell @ 85%
  static const Color textSoft = Color(0xD9FCF2EE);

  /// seashell @ 14%
  static const Color hairline = Color(0x24FCF2EE);

  /// seashell @ 40%
  static const Color border = Color(0x66FCF2EE);

  /// seashell @ 25%
  static const Color borderSoft = Color(0x40FCF2EE);

  /// bark @ 55%
  static const Color overlay = Color(0x8C100D0C);

  static const Color amberStart = Color(0xFF3A2418);
  static const Color amberEnd = Color(0xFF5C3A24);
  static const Color burgundyStart = Color(0xFF2A1218);
  static const Color burgundyEnd = Color(0xFF4A1C28);
  static const Color greenStart = Color(0xFF142018);
  static const Color greenEnd = Color(0xFF1E3A28);
  static const Color brownStart = Color(0xFF1C1410);
  static const Color brownEnd = Color(0xFF32241C);

  /// CSS `linear-gradient(160deg, start, end)`.
  static const LinearGradient amberPanel = LinearGradient(
    begin: Alignment(-0.34, -0.94),
    end: Alignment(0.34, 0.94),
    colors: [amberStart, amberEnd],
  );

  static const LinearGradient burgundyPanel = LinearGradient(
    begin: Alignment(-0.34, -0.94),
    end: Alignment(0.34, 0.94),
    colors: [burgundyStart, burgundyEnd],
  );

  static const LinearGradient greenPanel = LinearGradient(
    begin: Alignment(-0.34, -0.94),
    end: Alignment(0.34, 0.94),
    colors: [greenStart, greenEnd],
  );

  static const LinearGradient brownPanel = LinearGradient(
    begin: Alignment(-0.34, -0.94),
    end: Alignment(0.34, 0.94),
    colors: [brownStart, brownEnd],
  );
}
