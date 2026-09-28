/// Доступ до Django API для контенту застосунку.
abstract final class ApiConfig {
  /// Приклад: `--dart-define=API_BASE_URL=http://127.0.0.1:8001`
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://127.0.0.1:8001',
  );

  static Uri bundleUri() => Uri.parse('$baseUrl/api/v1/app/bundle/');
}
