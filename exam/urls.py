from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from main import sitemaps
from main.sitemaps import QuizSitemap


sitemaps = {
    "quiz": QuizSitemap,
}

urlpatterns = [
    path('', include('main.urls')),
    path('', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name="sitemap"),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)