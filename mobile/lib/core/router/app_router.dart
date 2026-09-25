import 'package:go_router/go_router.dart';

import '../../features/age_gate/presentation/age_gate_screen.dart';
import '../../features/booking/presentation/visit_screen.dart';
import '../../features/brands/presentation/brand_detail_screen.dart';
import '../../features/brands/presentation/brands_screen.dart';
import '../../features/contacts/presentation/contacts_screen.dart';
import '../../features/home/presentation/home_screen.dart';
import '../../features/house/presentation/house_screen.dart';
import '../../features/more/presentation/more_screen.dart';
import '../../features/offline/presentation/offline_screen.dart';
import '../../features/splash/presentation/splash_screen.dart';
import '../../shared/widgets/app_shell.dart';

GoRouter buildAppRouter() {
  return GoRouter(
    initialLocation: '/splash',
    routes: [
      GoRoute(path: '/splash', builder: (context, state) => const SplashScreen()),
      GoRoute(path: '/age', builder: (context, state) => const AgeGateScreen()),
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) => AppShell(navigationShell: navigationShell),
        branches: [
          StatefulShellBranch(
            routes: [
              GoRoute(path: '/home', builder: (context, state) => const HomeScreen()),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/brands',
                builder: (context, state) => const BrandsScreen(),
                routes: [
                  GoRoute(
                    path: ':id',
                    builder: (context, state) => BrandDetailScreen(brandId: state.pathParameters['id']!),
                  ),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/house',
                builder: (context, state) => const HouseScreen(),
                routes: [
                  GoRoute(path: 'visit', builder: (context, state) => const VisitScreen()),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(path: '/offline', builder: (context, state) => const OfflineScreen()),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/more',
                builder: (context, state) => const MoreScreen(),
                routes: [
                  GoRoute(path: 'contacts', builder: (context, state) => const ContactsScreen()),
                  GoRoute(
                    path: 'page/:id',
                    builder: (context, state) => InfoPageScreen(pageId: state.pathParameters['id']!),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    ],
  );
}
