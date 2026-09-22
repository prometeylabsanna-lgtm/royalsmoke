from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.pages.models import BlogPost


class StaticPagesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return [
            'pages:home',
            'pages:about',
            'pages:blog',
            'pages:faq',
            'catalog:list',
            'leads:contact',
            'leads:delivery',
        ]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
