from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'CMS / Сайт'

    def ready(self):
        from django.conf import settings

        from apps.core.admin_nav import build_unfold_navigation

        unfold = getattr(settings, 'UNFOLD', None)
        if isinstance(unfold, dict):
            sidebar = unfold.setdefault('SIDEBAR', {})
            sidebar['navigation'] = build_unfold_navigation()
