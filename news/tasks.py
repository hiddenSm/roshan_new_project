import os, sys

if 'flower' not in sys.argv:
    from twisted.internet import asyncioreactor
    try:
        asyncioreactor.install()
    except Exception as e:
        # print(e)
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roshan_news.settings')

import logging, crochet
from crochet import setup
from celery import shared_task
from scrapy.signals import item_scraped 
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from news.models import News
from news_scraper.news_scraper.spiders.zoomit import ZoomitSpider

logger = logging.getLogger(__name__)


setup()

@shared_task
def crawl_zoomit():
    items = []

    def collect_item(item, response, spider):
        logger.info(f"date11 {item['created_at']}")
        items.append({
            'title': item['title'],
            'content': item['content'][:100] + '...' if len(item['content']) > 100 else item['content'],
            'tags': item['tags'],
            'source': item['source'],
            'created_at': item['created_at']
        })
        return items

    try:
        crochet.setup()
        runner = CrawlerRunner(get_project_settings())

        @crochet.run_in_reactor
        def run_spider():
            crawler = runner.create_crawler(ZoomitSpider)
            crawler.signals.connect(collect_item, signal=item_scraped)
            deferred = runner.crawl(crawler)
            return deferred
        
        eventual_result = run_spider()
        eventual_result.wait(timeout=100)

        saved_count = 0
        for item in items:
            try:  
                if News.objects.filter(title=item['title']).exists():
                    logger.info(f"خبر تکراری: {item['title']}")
                    continue

                logger.info(f"date: {item['created_at']}")
                news, created = News.objects.get_or_create(
                    title=item['title'],
                    defaults={
                        'content': item['content'],
                        'source': item['source'],
                        'created_at': item['created_at']
                    }
                )
                for tag in item['tags']:
                    tag_name = tag.strip()
                    if tag_name:
                        news.tags.add(tag_name)
                    saved_count += 1
                    news.save()
                    logger.info(f"خبر جدید ذخیره شد: {news.title}")

            except Exception as e:
                logger.error(f"خطا در ذخیره‌سازی خبر: {str(e)}")

        logger.info(f"استخراج موفق! {saved_count} خبر ذخیره شد.")
        return f"استخراج موفق! {saved_count} خبر ذخیره شد."

    except Exception as e:
        logger.error(f"خطا در اجرای تسک: {str(e)}")
        return f"خطا در اجرای تسک: {str(e)}"
