from django.urls import path
from .views import NewsListView, NewsCreateView, CrawlView #, ScrapeNewsView, ScrapyNewsView


urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    # path('news/scrape/', ScrapeNewsView.as_view(), name='news-scrape'),
    # path('scrapy-news/', ScrapyNewsView.as_view(), name='scrapy-news'),
    path('crawl/', CrawlView.as_view(), name='crawl'),
]
