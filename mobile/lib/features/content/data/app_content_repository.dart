import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../../../core/config/api_config.dart';
import '../domain/app_content.dart';
import 'bundle_parser.dart';
import 'fallback_bundle.dart';

const _cacheKey = 'rs_app_content_bundle_v1';
const _cacheAtKey = 'rs_app_content_bundle_at_v1';

class AppContentRepository {
  AppContentRepository({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Future<AppContentBundle> load({bool forceNetwork = false}) async {
    final prefs = await SharedPreferences.getInstance();

    if (!forceNetwork) {
      final cached = prefs.getString(_cacheKey);
      final atMs = prefs.getInt(_cacheAtKey);
      if (cached != null && cached.isNotEmpty) {
        try {
          final map = jsonDecode(cached) as Map<String, dynamic>;
          // Паралельно оновлюємо з мережі у фоні не блокуємо — нижче спробуємо network.
          final bundle = parseAppBundle(
            map,
            updatedAt: atMs == null ? null : DateTime.fromMillisecondsSinceEpoch(atMs),
          );
          // Спробувати свіжий bundle; якщо fail — повернути кеш.
          final fresh = await _tryFetchAndCache(prefs);
          return fresh ?? bundle;
        } catch (_) {
          // fall through
        }
      }
    }

    final fresh = await _tryFetchAndCache(prefs);
    if (fresh != null) return fresh;

    final cached = prefs.getString(_cacheKey);
    if (cached != null && cached.isNotEmpty) {
      try {
        final map = jsonDecode(cached) as Map<String, dynamic>;
        final atMs = prefs.getInt(_cacheAtKey);
        return parseAppBundle(
          map,
          updatedAt: atMs == null ? null : DateTime.fromMillisecondsSinceEpoch(atMs),
        );
      } catch (_) {}
    }

    return buildFallbackBundle();
  }

  Future<AppContentBundle?> _tryFetchAndCache(SharedPreferences prefs) async {
    try {
      final response = await _client
          .get(ApiConfig.bundleUri())
          .timeout(const Duration(seconds: 8));
      if (response.statusCode != 200) return null;
      final map = jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
      final now = DateTime.now();
      await prefs.setString(_cacheKey, jsonEncode(map));
      await prefs.setInt(_cacheAtKey, now.millisecondsSinceEpoch);
      return parseAppBundle(map, updatedAt: now);
    } catch (_) {
      return null;
    }
  }
}
