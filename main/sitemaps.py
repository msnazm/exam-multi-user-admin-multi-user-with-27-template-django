from django.contrib.sitemaps import Sitemap
from main.models import Quiz

class QuizSitemap(Sitemap):
    changefreq = "weekly" 
    priority = 0.8

    def items(self):
        return Quiz.objects.all()

    def lastmod(self, obj):
        return obj.create_date