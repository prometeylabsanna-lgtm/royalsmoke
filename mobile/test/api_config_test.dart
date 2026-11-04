import 'package:flutter_test/flutter_test.dart';
import 'package:royal_smoke/core/config/api_config.dart';

void main() {
  test('bundle URI завжди має шлях /api/v1/app/bundle/', () {
    final uri = ApiConfig.bundleUri('uk');
    final root = ApiConfig.baseUrl.endsWith('/')
        ? ApiConfig.baseUrl.substring(0, ApiConfig.baseUrl.length - 1)
        : ApiConfig.baseUrl;

    expect(uri.path, '/api/v1/app/bundle/');
    expect(uri.queryParameters, {'lang': 'uk'});
    expect(uri.origin, Uri.parse(root).origin);
    expect(uri.toString(), '$root/api/v1/app/bundle/?lang=uk');
  });
}
