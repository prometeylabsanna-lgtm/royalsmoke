import 'package:flutter/material.dart';
import 'package:royal_smoke/core/router/app_router.dart';
import 'package:royal_smoke/core/theme/app_theme.dart';

class RoyalSmokeApp extends StatefulWidget {
  const RoyalSmokeApp({super.key});

  @override
  State<RoyalSmokeApp> createState() => _RoyalSmokeAppState();
}

class _RoyalSmokeAppState extends State<RoyalSmokeApp> {
  late final _router = buildAppRouter();

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Royal Smoke',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.dark,
      routerConfig: _router,
    );
  }
}
