from django.test import TestCase
from .models import News

# Create your tests here.

class NewsModelTest(TestCase):
    def setUp(self):
        News.objects.create(title="Test News", content="This is a test news.", tags="tech,science", source="Test Source")

    def test_news_creation(self):
        news = News.objects.get(title="Test News")
        self.assertEqual(news.content, "This is a test news.")
        self.assertEqual(news.tags, "tech,science")
        self.assertEqual(news.source, "Test Source")
