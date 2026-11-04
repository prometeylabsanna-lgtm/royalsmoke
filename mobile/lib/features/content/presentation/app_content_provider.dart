import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../data/app_content_repository.dart';
import '../data/fallback_bundle.dart';
import '../domain/app_content.dart';

final appContentRepositoryProvider = Provider<AppContentRepository>((ref) {
  return AppContentRepository();
});

class AppContentNotifier extends AsyncNotifier<AppContentBundle> {
  @override
  Future<AppContentBundle> build() async {
    final locale = ref.watch(appLocaleProvider);
    final l10n = lookupAppLocalizations(locale);
    final repo = ref.read(appContentRepositoryProvider);
    try {
      return await repo.load(lang: apiLanguageCode(locale), l10n: l10n);
    } catch (_) {
      return buildFallbackBundle(l10n);
    }
  }

  Future<void> refresh() async {
    final locale = ref.read(appLocaleProvider);
    final l10n = lookupAppLocalizations(locale);
    state = const AsyncLoading();
    state = AsyncData(
      await ref.read(appContentRepositoryProvider).load(
            lang: apiLanguageCode(locale),
            l10n: l10n,
            forceNetwork: true,
          ),
    );
  }
}

final appContentProvider =
    AsyncNotifierProvider<AppContentNotifier, AppContentBundle>(AppContentNotifier.new);

/// Синхронний доступ: remote / кеш / fallback.
AppContentBundle watchContent(WidgetRef ref) {
  final locale = ref.watch(appLocaleProvider);
  final l10n = lookupAppLocalizations(locale);
  return ref.watch(appContentProvider).asData?.value ?? buildFallbackBundle(l10n);
}
