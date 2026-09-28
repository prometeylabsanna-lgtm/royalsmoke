import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/partner_catalog.dart';
import '../domain/partner_brand.dart';

/// Збережені бренди (демо: два партнери на старті).
class SavedBrandsNotifier extends Notifier<Set<String>> {
  @override
  Set<String> build() => {'oliva', 'perdomo'};

  bool contains(String id) => state.contains(id);

  void toggle(String id) {
    final next = {...state};
    if (!next.add(id)) next.remove(id);
    state = next;
  }
}

final savedBrandsProvider =
    NotifierProvider<SavedBrandsNotifier, Set<String>>(SavedBrandsNotifier.new);

final savedBrandListProvider = Provider<List<PartnerBrand>>((ref) {
  final ids = ref.watch(savedBrandsProvider);
  return PartnerCatalog.brands.where((b) => ids.contains(b.id)).toList();
});
