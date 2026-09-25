import 'package:flutter/material.dart';

enum BrandPanel { amber, burgundy, green, brown }

class BrandFact {
  const BrandFact({required this.label, required this.value});

  final String label;
  final String value;
}

/// Довідковий запис партнера. Без ціни, залишку і покупки.
class PartnerBrand {
  const PartnerBrand({
    required this.id,
    required this.mono,
    required this.shortName,
    required this.name,
    required this.country,
    required this.panel,
    required this.imageAsset,
    required this.heritage,
    required this.facts,
    required this.lines,
  });

  final String id;
  final String mono;
  final String shortName;
  final String name;
  final String country;
  final BrandPanel panel;
  final String imageAsset;
  final String heritage;
  final List<BrandFact> facts;
  final List<String> lines;

  LinearGradient get gradient => switch (panel) {
        BrandPanel.amber => const LinearGradient(
            begin: Alignment(-0.34, -0.94),
            end: Alignment(0.34, 0.94),
            colors: [Color(0xFF3A2418), Color(0xFF5C3A24)],
          ),
        BrandPanel.burgundy => const LinearGradient(
            begin: Alignment(-0.34, -0.94),
            end: Alignment(0.34, 0.94),
            colors: [Color(0xFF2A1218), Color(0xFF4A1C28)],
          ),
        BrandPanel.green => const LinearGradient(
            begin: Alignment(-0.34, -0.94),
            end: Alignment(0.34, 0.94),
            colors: [Color(0xFF142018), Color(0xFF1E3A28)],
          ),
        BrandPanel.brown => const LinearGradient(
            begin: Alignment(-0.34, -0.94),
            end: Alignment(0.34, 0.94),
            colors: [Color(0xFF1C1410), Color(0xFF32241C)],
          ),
      };
}
