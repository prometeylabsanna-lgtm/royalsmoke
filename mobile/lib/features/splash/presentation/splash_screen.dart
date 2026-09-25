import 'dart:async';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_chrome.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key, this.autoAdvance = const Duration(milliseconds: 1600)});

  final Duration autoAdvance;

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  bool _left = false;
  late final _timer = Timer(widget.autoAdvance, _open);

  @override
  void initState() {
    super.initState();
    _timer;
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  void _open() {
    if (!mounted || _left) return;
    _left = true;
    context.go('/age');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bark,
      body: Stack(
        children: [
          const Positioned.fill(child: _BarkGrain()),
          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const RsSeal(size: 120),
                const SizedBox(height: 28),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: FittedBox(
                    fit: BoxFit.scaleDown,
                    child: Padding(
                      padding: const EdgeInsets.only(left: 24 * 0.32),
                      child: Text(
                        'ROYAL SMOKE',
                        style: TextStyle(
                          fontFamily: AppTextStyles.family,
                          fontSize: 24,
                          fontWeight: FontWeight.w600,
                          height: 1.1,
                          letterSpacing: 24 * 0.32,
                          color: AppColors.seashell,
                        ),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 28),
                Text(
                  'ДОВІДНИК БРЕНДУ',
                  style: AppTextStyles.kicker.copyWith(letterSpacing: 11 * 0.34),
                ),
              ],
            ),
          ),
          Positioned(
            left: 0,
            right: 0,
            bottom: 48 + MediaQuery.paddingOf(context).bottom,
            child: Column(
              children: [
                TextButton(
                  onPressed: _open,
                  style: TextButton.styleFrom(
                    foregroundColor: AppColors.seashell,
                    minimumSize: const Size(0, 48),
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                  ),
                  child: Text(
                    'ВІДКРИТИ',
                    style: TextStyle(
                      fontFamily: AppTextStyles.family,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      letterSpacing: 12 * 0.24,
                      color: AppColors.seashell,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const RsAgeBadge(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _BarkGrain extends StatelessWidget {
  const _BarkGrain();

  @override
  Widget build(BuildContext context) {
    return const DecoratedBox(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF14100E), AppColors.bark],
        ),
      ),
    );
  }
}
