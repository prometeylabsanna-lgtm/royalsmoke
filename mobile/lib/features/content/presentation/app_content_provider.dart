import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../brands/domain/partner_brand.dart';
import '../data/app_content_repository.dart';
import '../data/fallback_bundle.dart';
import '../domain/app_content.dart';

final appContentRepositoryProvider = Provider<AppContentRepository>((ref) {
  return AppContentRepository();
});

class AppContentNotifier extends AsyncNotifier<AppContentBundle> {
  @override
  Future<AppContentBundle> build() async {
    final repo = ref.read(appContentRepositoryProvider);
    try {
      return await repo.load();
    } catch (_) {
      return buildFallbackBundle();
    }
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = AsyncData(await ref.read(appContentRepositoryProvider).load(forceNetwork: true));
  }
}

final appContentProvider =
    AsyncNotifierProvider<AppContentNotifier, AppContentBundle>(AppContentNotifier.new);

/// Синхронний доступ: remote / кеш / fallback.
AppContentBundle watchContent(WidgetRef ref) {
  return ref.watch(appContentProvider).asData?.value ?? buildFallbackBundle();
}

final appBrandsProvider = Provider<List<PartnerBrand>>((ref) {
  return ref.watch(appContentProvider).asData?.value.brands ?? buildFallbackBundle().brands;
});
