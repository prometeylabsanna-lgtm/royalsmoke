import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'rs_chrome.dart';

class AppShell extends StatelessWidget {
  const AppShell({super.key, required this.navigationShell});

  final StatefulNavigationShell navigationShell;

  void _onTab(RsTab tab) {
    // Завжди відкриваємо корінь вкладки: після картки бренду «Бренди»
    // знову показує список, а не залишений detail.
    navigationShell.goBranch(tab.index, initialLocation: true);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Material(
        color: Colors.transparent,
        child: navigationShell,
      ),
      bottomNavigationBar: RsTabBar(
        current: RsTab.values[navigationShell.currentIndex],
        onChanged: _onTab,
      ),
    );
  }
}
