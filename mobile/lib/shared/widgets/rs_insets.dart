import 'dart:math' as math;

import 'package:flutter/widgets.dart';

/// Верхній системний інсет: статус-бар, notch, Dynamic Island.
double rsTopInset(BuildContext context) {
  final media = MediaQuery.of(context);
  return math.max(media.padding.top, media.viewPadding.top);
}

/// Нижній системний інсет: home indicator або жест Android.
/// Поки відкрита клавіатура, лишаємо [MediaQueryData.padding] — його вже з’їв viewInsets.
double rsBottomInset(BuildContext context) {
  final media = MediaQuery.of(context);
  if (media.viewInsets.bottom > 0) return media.padding.bottom;
  return math.max(
    media.padding.bottom,
    math.max(media.viewPadding.bottom, media.systemGestureInsets.bottom),
  );
}

EdgeInsets rsSafeEdges(
  BuildContext context, {
  bool left = true,
  bool top = true,
  bool right = true,
  bool bottom = false,
}) {
  final media = MediaQuery.of(context);
  return EdgeInsets.fromLTRB(
    left ? math.max(media.padding.left, media.viewPadding.left) : 0,
    top ? rsTopInset(context) : 0,
    right ? math.max(media.padding.right, media.viewPadding.right) : 0,
    bottom ? rsBottomInset(context) : 0,
  );
}

/// Тримає вміст нижче статус-бару / вирізу і з боків від notch.
/// Нижній жест лишається таб-бару, щоб не подвоювати відступ.
///
/// Власний зазор екрана (24 / 8) залишається всередині скролу:
/// між системним інсетом і брівкою він той самий, що й був від краю.
class RsSafeBody extends StatelessWidget {
  const RsSafeBody({super.key, required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    final edges = rsSafeEdges(context);
    if (edges == EdgeInsets.zero) return child;
    return Padding(
      padding: edges,
      child: MediaQuery.removePadding(
        context: context,
        removeLeft: edges.left > 0,
        removeTop: edges.top > 0,
        removeRight: edges.right > 0,
        child: child,
      ),
    );
  }
}
