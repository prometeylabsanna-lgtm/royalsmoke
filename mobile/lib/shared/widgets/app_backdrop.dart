import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/constants/app_images.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_theme.dart';
import 'backdrop_motion.dart';

/// Спільний фон під усіма маршрутами. Контролери живуть тут і не
/// скидаються, коли змінюється вкладка чи сторінка.
class AppBackdrop extends StatefulWidget {
  const AppBackdrop({super.key, required this.child});

  final Widget child;

  @override
  AppBackdropState createState() => AppBackdropState();
}

class AppBackdropState extends State<AppBackdrop>
    with TickerProviderStateMixin {
  late final AnimationController _kenBurns;
  late final AnimationController _glow;
  late final CurvedAnimation _kenBurnsT;
  late final CurvedAnimation _glowT;
  bool? _reduceMotion;
  bool _precached = false;

  @visibleForTesting
  double get kenBurnsT => _kenBurns.value;

  @visibleForTesting
  bool get motionRunning => _kenBurns.isAnimating;

  @override
  void initState() {
    super.initState();
    _kenBurns = AnimationController(
      vsync: this,
      duration: BackdropMotion.kenBurnsDuration,
    );
    _glow = AnimationController(
      vsync: this,
      duration: BackdropMotion.glowDuration,
    );
    _kenBurnsT = CurvedAnimation(
      parent: _kenBurns,
      curve: Curves.easeInOut,
      reverseCurve: Curves.easeInOut,
    );
    _glowT = CurvedAnimation(
      parent: _glow,
      curve: Curves.easeInOut,
      reverseCurve: Curves.easeInOut,
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _syncMotion(MediaQuery.disableAnimationsOf(context));
    if (_precached) return;
    _precached = true;
    precacheImage(const AssetImage(AppImages.appBackground), context);
  }

  void _syncMotion(bool reduce) {
    // Знімки стора збираються з --dart-define=FORCE_REDUCE_MOTION=true,
    // бо симулятор не завжди прокидає Reduce Motion у Flutter.
    const forced = bool.fromEnvironment('FORCE_REDUCE_MOTION');
    reduce = forced || reduce;
    if (_reduceMotion == reduce) return;
    _reduceMotion = reduce;
    if (reduce) {
      _kenBurns.stop();
      _glow.stop();
      _kenBurns.value = 0;
      _glow.value = 0;
      return;
    }
    _kenBurns.repeat(reverse: true);
    _glow.repeat(reverse: true);
  }

  @override
  void dispose() {
    _kenBurnsT.dispose();
    _glowT.dispose();
    _kenBurns.dispose();
    _glow.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.sizeOf(context);
    return AnnotatedRegion<SystemUiOverlayStyle>(
      value: AppTheme.overlay,
      child: Stack(
        fit: StackFit.expand,
        children: [
          const ColoredBox(color: AppColors.canvas),
          if (size.width > 0 && size.height > 0) ...[
            _KenBurnsPlate(size: size, motion: _kenBurnsT),
            const IgnorePointer(
              child: ColoredBox(color: AppColors.backdropDim),
            ),
            _BottomMask(height: size.height),
            _TopScrim(height: size.height),
            _GoldGlow(height: size.height, glow: _glowT),
          ],
          widget.child,
        ],
      ),
    );
  }
}

class _KenBurnsPlate extends StatelessWidget {
  const _KenBurnsPlate({required this.size, required this.motion});

  final Size size;
  final Animation<double> motion;

  static const double _bleed = 2;

  @override
  Widget build(BuildContext context) {
    final plateWidth = size.width + _bleed * 2;
    final plateHeight = plateWidth * BackdropMotion.imageAspect;
    return Positioned(
      top: 0,
      left: -_bleed,
      width: plateWidth,
      height: plateHeight,
      child: AnimatedBuilder(
        animation: motion,
        builder: (context, child) {
          final frame = BackdropMotion.at(
            t: motion.value,
            width: size.width,
            imageHeight: plateHeight,
          );
          return Transform.translate(
            offset: Offset(frame.dx, frame.dy),
            child: Transform.scale(
              scale: frame.scale,
              alignment: Alignment.topCenter,
              child: child,
            ),
          );
        },
        child: const RepaintBoundary(child: _StillPlate()),
      ),
    );
  }
}

class _StillPlate extends StatelessWidget {
  const _StillPlate();

  @override
  Widget build(BuildContext context) {
    return const Stack(
      fit: StackFit.expand,
      children: [
        Image(
          image: AssetImage(AppImages.appBackground),
          fit: BoxFit.fitWidth,
          alignment: Alignment.topCenter,
          filterQuality: FilterQuality.medium,
          gaplessPlayback: true,
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: FractionallySizedBox(
            heightFactor: 0.25,
            widthFactor: 1,
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [AppColors.canvasClear, AppColors.canvas],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class _BottomMask extends StatelessWidget {
  const _BottomMask({required this.height});

  final double height;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: 0,
      right: 0,
      bottom: 0,
      height: height * 0.30 < 180 ? 180 : height * 0.30,
      child: const IgnorePointer(
        child: DecoratedBox(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                AppColors.canvasClear,
                AppColors.canvas,
                AppColors.canvas,
              ],
              stops: [0, 0.62, 1],
            ),
          ),
        ),
      ),
    );
  }
}

class _TopScrim extends StatelessWidget {
  const _TopScrim({required this.height});

  final double height;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: 0,
      left: 0,
      right: 0,
      height: height * 0.46,
      child: const IgnorePointer(
        child: DecoratedBox(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Color(0x6B1E1009),
                Color(0x331E1009),
                AppColors.canvasClear,
              ],
              stops: [0, 0.42, 1],
            ),
          ),
        ),
      ),
    );
  }
}

class _GoldGlow extends StatelessWidget {
  const _GoldGlow({required this.height, required this.glow});

  final double height;
  final Animation<double> glow;

  @override
  Widget build(BuildContext context) {
    return Positioned(
      top: 0,
      left: 0,
      right: 0,
      height: height * 0.62,
      child: IgnorePointer(
        child: RepaintBoundary(
          child: AnimatedBuilder(
            animation: glow,
            builder: (context, child) {
              final opacity = (glow.value * BackdropMotion.glowPeakOpacity)
                  .clamp(0.0, BackdropMotion.glowPeakOpacity);
              if (opacity == 0) return const SizedBox.shrink();
              return Opacity(opacity: opacity, child: child);
            },
            child: const DecoratedBox(
              decoration: BoxDecoration(
                gradient: RadialGradient(
                  center: Alignment(0, -0.72),
                  radius: 1.05,
                  colors: [AppColors.gold, Color(0x00C99A44)],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
