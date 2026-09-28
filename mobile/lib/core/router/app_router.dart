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
import 'rs_page.dart';

GoRouter buildAppRouter() {
  return GoRouter(
    initialLocation: '/splash',
    routes: [
      GoRoute(
        path: '/splash',
        pageBuilder: (context, state) => rsOpaquePage(
          key: state.pageKey,
          child: const SplashScreen(),
        ),
      ),
      GoRoute(
        path: '/age',
        pageBuilder: (context, state) => rsOpaquePage(
          key: state.pageKey,
          child: const AgeGateScreen(),
        ),
      ),
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) => AppShell(navigationShell: navigationShell),
        branches: [
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/home',
                pageBuilder: (context, state) => rsOpaquePage(
                  key: state.pageKey,
                  child: const HomeScreen(),
                ),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/brands',
                pageBuilder: (context, state) => rsOpaquePage(
                  key: state.pageKey,
                  child: const BrandsScreen(),
                ),
                routes: [
                  GoRoute(
                    path: ':id',
                    pageBuilder: (context, state) => rsOpaquePage(
                      key: state.pageKey,
                      child: BrandDetailScreen(brandId: state.pathParameters['id']!),
                    ),
                  ),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/house',
                pageBuilder: (context, state) => rsOpaquePage(
                  key: state.pageKey,
                  child: const HouseScreen(),
                ),
                routes: [
                  GoRoute(
                    path: 'visit',
                    pageBuilder: (context, state) => rsOpaquePage(
                      key: state.pageKey,
                      child: const VisitScreen(),
                    ),
                  ),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/offline',
                pageBuilder: (context, state) => rsOpaquePage(
                  key: state.pageKey,
                  child: const OfflineScreen(),
                ),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/more',
                pageBuilder: (context, state) => rsOpaquePage(
                  key: state.pageKey,
                  child: const MoreScreen(),
                ),
                routes: [
                  GoRoute(
                    path: 'contacts',
                    pageBuilder: (context, state) => rsOpaquePage(
                      key: state.pageKey,
                      child: const ContactsScreen(),
                    ),
                  ),
                  GoRoute(
                    path: 'page/:id',
                    pageBuilder: (context, state) => rsOpaquePage(
                      key: state.pageKey,
                      child: InfoPageScreen(pageId: state.pathParameters['id']!),
                    ),
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
