import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../features/brands/domain/partner_brand.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_brand.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_fields.dart';
import '../../../shared/widgets/rs_rows.dart';

class BrandsScreen extends ConsumerStatefulWidget {
  const BrandsScreen({super.key});

  @override
  ConsumerState<BrandsScreen> createState() => _BrandsScreenState();
}

class _BrandsScreenState extends ConsumerState<BrandsScreen> {
  final _query = TextEditingController();

  @override
  void dispose() {
    _query.dispose();
    super.dispose();
  }

  List<PartnerBrand> _visible(List<PartnerBrand> all) {
    final q = _query.text.trim().toLowerCase();
    if (q.isEmpty) return all;
    return all
        .where((b) => '${b.name} ${b.shortName}'.toLowerCase().contains(q))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final brands = _visible(ref.watch(appBrandsProvider));
    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 24, AppSizes.padX, AppSizes.s24),
      children: [
        const RsPageHeading(kicker: 'Партнери дому', title: 'Бренди'),
        const SizedBox(height: AppSizes.s24),
        RsSearchField(controller: _query, onChanged: (_) => setState(() {})),
        const SizedBox(height: AppSizes.s16),
        const Align(alignment: Alignment.centerLeft, child: RsChip(label: 'Усі', selected: true)),
        const SizedBox(height: AppSizes.s24),
        if (brands.isEmpty)
          const Padding(
            padding: EdgeInsets.only(top: 80),
            child: RsEmptySearch(),
          )
        else
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: brands.length,
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              mainAxisSpacing: 24,
              crossAxisSpacing: 14,
              childAspectRatio: 0.72,
            ),
            itemBuilder: (context, index) {
              final brand = brands[index];
              return RsBrandCell(
                brand: brand,
                onTap: () => context.go('/brands/${brand.id}'),
              );
            },
          ),
      ],
    );
  }
}
