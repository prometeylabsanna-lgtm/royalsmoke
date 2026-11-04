import 'package:flutter/foundation.dart';

/// Доступ до Django API для контенту застосунку.
abstract final class ApiConfig {
  /// Приклад: `--dart-define=API_BASE_URL=https://royalsmk.com.ua`
  /// Непорожній dart-define перекриває і release, і debug.
  static const String _fromEnvironment = String.fromEnvironment('API_BASE_URL');

  static const String _releaseDefault = 'https://royalsmk.com.ua';
  static const String _debugDefault = 'http://127.0.0.1:8001';

  static const String baseUrl = _fromEnvironment != ''
      ? _fromEnvironment
      : (kReleaseMode ? _releaseDefault : _debugDefault);

  static Uri bundleUri(String lang) {
    final root = baseUrl.endsWith('/')
        ? baseUrl.substring(0, baseUrl.length - 1)
        : baseUrl;
    return Uri.parse('$root/api/v1/app/bundle/').replace(
      queryParameters: {'lang': lang},
    );
  }
}
