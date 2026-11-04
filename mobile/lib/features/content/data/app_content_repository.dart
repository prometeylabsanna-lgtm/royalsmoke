import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:royal_smoke/l10n/app_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../core/config/api_config.dart';
import '../domain/app_content.dart';
import 'bundle_parser.dart';
import 'fallback_bundle.dart';

String _cacheKey(String lang) => 'rs_app_content_bundle_v3_$lang';
String _cacheAtKey(String lang) => 'rs_app_content_bundle_at_v3_$lang';

class AppContentRepository {
  AppContentRepository({http.Client? client})
    : _client = client ?? http.Client();

  final http.Client _client;

  Future<AppContentBundle> load({
    required String lang,
    required AppLocalizations l10n,
    bool forceNetwork = false,
  }) async {
    final prefs = await _prefs();
    final cacheKey = _cacheKey(lang);
    final cacheAtKey = _cacheAtKey(lang);

    if (prefs != null && !forceNetwork) {
      final cached = prefs.getString(cacheKey);
      final atMs = prefs.getInt(cacheAtKey);
      if (cached != null && cached.isNotEmpty) {
        try {
          final map = jsonDecode(cached) as Map<String, dynamic>;
          // Паралельно оновлюємо з мережі у фоні не блокуємо — нижче спробуємо network.
          final bundle = parseAppBundle(
            map,
            updatedAt: atMs == null
                ? null
                : DateTime.fromMillisecondsSinceEpoch(atMs),
          );
          final fresh = await _tryFetchAndCache(prefs, lang);
          return fresh ?? bundle;
        } catch (_) {
          // fall through
        }
      }
    }

    final fresh = prefs == null ? null : await _tryFetchAndCache(prefs, lang);
    if (fresh != null) return fresh;

    if (prefs != null) {
      final cached = prefs.getString(cacheKey);
      if (cached != null && cached.isNotEmpty) {
        try {
          final map = jsonDecode(cached) as Map<String, dynamic>;
          final atMs = prefs.getInt(cacheAtKey);
          return parseAppBundle(
            map,
            updatedAt: atMs == null
                ? null
                : DateTime.fromMillisecondsSinceEpoch(atMs),
          );
        } catch (_) {}
      }
    }

    return buildFallbackBundle(l10n);
  }

  Future<SharedPreferences?> _prefs() async {
    try {
      return await SharedPreferences.getInstance();
    } catch (_) {
      return null;
    }
  }

  Future<AppContentBundle?> _tryFetchAndCache(
    SharedPreferences prefs,
    String lang,
  ) async {
    try {
      final response = await _client
          .get(ApiConfig.bundleUri(lang), headers: {'Accept-Language': lang})
          .timeout(const Duration(seconds: 8));
      if (response.statusCode != 200) return null;
      final map =
          jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
      final now = DateTime.now();
      await prefs.setString(_cacheKey(lang), jsonEncode(map));
      await prefs.setInt(_cacheAtKey(lang), now.millisecondsSinceEpoch);
      return parseAppBundle(map, updatedAt: now);
    } catch (_) {
      return null;
    }
  }
}
