import crochet, os
# from crochet import setup
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.signals import item_scraped 

from .models import News
from .serializers import NewsSerializer
from news_scraper.news_scraper import settings as scrapy_settinga
from news_scraper.news_scraper.spiders.zoomit import ZoomitSpider


# Create your views here.

# os.environ['SCRAPY_SETTINGS_MODULE'] = 'news_scraper.news_scraper.settings'
# scrapy_settinga.set('ITEM_PIPELINES', {'news_scraper.pipelines.DjangoPipeline': 300})

# setup()
crochet.setup()

class CrawlView(APIView):
    def get(self, request):
        items = []
        def collect_item(item, response, spider):
            items.append({
                'title': item['title'],
                'content': item['content'][:100] + '...' if len(item['content']) > 100 else item['content'],
                'tags': item['tags'],
                'source': item['source'],
                'created_at': timezone.now()
            })

        try:
            runner = CrawlerRunner(get_project_settings())

            @crochet.run_in_reactor
            def run_spider():
                crawler = runner.create_crawler(ZoomitSpider)
                crawler.signals.connect(collect_item, signal=item_scraped)
                deferred = runner.crawl(crawler)
                return deferred

            eventual_result = run_spider()
            eventual_result.wait(timeout=100)

            for item in items:
                news, created = News.objects.get_or_create(
                    title=item['title'],
                    defaults={
                        'content': item['content'],
                        # 'tags': item['tags'],
                        'source': item['source'],
                        'created_at': timezone.now()
                    }
                )
                for tag in item['tags']:
                    tag_name = tag.strip()
                    if tag_name:
                        news.tags.add(tag_name)

            return Response({
                'message': f'استخراج موفق! {len(items)} خبر ذخیره شد.',
                'news': items
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewsListView(ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all().order_by('-created_at')
        tags = self.request.query_params.get('tags')
        # include_keywords = self.request.query_params.getlist('include')
        # exclude_keywords = self.request.query_params.getlist('exclude')
        include_keywords = self.request.query_params.get('include')
        exclude_keywords = self.request.query_params.get('exclude')

        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if tag_list:
                queryset = queryset.filter(tags__name__in=tag_list).distinct()

        if include_keywords:
            cleaned_keywords = [keyword.strip() for keyword in include_keywords.split(',') if keyword.strip()]
            include_query = Q()
            for keyword in cleaned_keywords:
                include_query |= Q(content__icontains=keyword) | Q(title__icontains=keyword)
            queryset = queryset.filter(include_query)

        if exclude_keywords:
            cleaned_exclude_keywords = [keyword.strip() for keyword in exclude_keywords.split(',') if keyword.strip()]
            exclude_query = Q()
            for keyword in cleaned_exclude_keywords:
                exclude_query |= Q(content__icontains=keyword) | Q(title__icontains=keyword)
            queryset = queryset.exclude(exclude_query)

        return queryset
    
class NewsCreateView(APIView):
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'خبر با موفقیت ذخیره شد.',
                'news': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
