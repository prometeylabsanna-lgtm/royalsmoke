import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../../core/constants/app_copy.dart';
import '../../core/constants/app_sizes.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';

/// Карта місця дому (OSM) без стороннього API-ключа.
class RsVenueMap extends StatelessWidget {
  const RsVenueMap({
    super.key,
    this.height = 190,
    this.lat = AppCopy.contactLat,
    this.lng = AppCopy.contactLng,
  });

  final double height;
  final double lat;
  final double lng;

  @override
  Widget build(BuildContext context) {
    final point = LatLng(lat, lng);
    return ClipRRect(
      borderRadius: BorderRadius.circular(AppSizes.radiusSearch),
      child: SizedBox(
        height: height,
        child: Stack(
          children: [
            FlutterMap(
              options: MapOptions(
                initialCenter: point,
                initialZoom: 15.5,
                interactionOptions: const InteractionOptions(
                  flags: InteractiveFlag.pinchZoom | InteractiveFlag.drag,
                ),
              ),
              children: [
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  userAgentPackageName: 'com.royalsmoke.royal_smoke',
                ),
                MarkerLayer(
                  markers: [
                    Marker(
                      point: point,
                      width: 36,
                      height: 36,
                      child: const Icon(Icons.location_on, color: AppColors.gold, size: 36),
                    ),
                  ],
                ),
              ],
            ),
            Positioned(
              right: 10,
              bottom: 8,
              child: Text(
                'МАПА',
                style: AppTextStyles.kicker.copyWith(
                  color: AppColors.seashell.withValues(alpha: 0.7),
                  shadows: const [Shadow(blurRadius: 6, color: Color(0x88000000))],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
