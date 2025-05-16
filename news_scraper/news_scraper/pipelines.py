# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class NewsScraperPipeline:
#     def process_item(self, item, spider):
#         return item

from asgiref.sync import sync_to_async
from django.utils import timezone
from news.models import News


class DjangoPipeline:
    @sync_to_async
    def save_news(self, item):
        try:
            news, created = News.objects.get_or_create(
                title=item['title'],
                defaults={
                    'content': item['content'],
                    'source': item['source'],
                    'created_at': timezone.now()
                }
            )
            for tag in item['tags']:
                tag_name = tag.strip()
                if tag_name:
                    news.tags.add(tag_name)
            return news
        
        except Exception as e:
            raise e

    async def process_item(self, item, spider):
        await self.save_news(item)
        return item