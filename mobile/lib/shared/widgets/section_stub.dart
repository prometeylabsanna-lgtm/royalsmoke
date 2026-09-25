import 'package:flutter/material.dart';

import '../../core/constants/app_sizes.dart';
import 'rs_chrome.dart';

/// Тимчасовий екран розділу. Наповнення — на кроці 4.
class SectionStub extends StatelessWidget {
  const SectionStub({super.key, required this.kicker, required this.title});

  final String kicker;
  final String title;

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      bottom: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
        child: RsPageHeading(kicker: kicker, title: title),
      ),
    );
  }
}
