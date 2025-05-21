# import scrapy


# class ZoomitSpider(scrapy.Spider):
#     name = "zoomit"
#     allowed_domains = ["zoomit.ir"]
#     start_urls = ["https://zoomit.ir"]

#     def parse(self, response):
#         pass

import scrapy
from ..items import NewsItem
from .scrapy_utils import jalali_to_gregorian


class ZoomitSpider(scrapy.Spider):
    name = 'zoomit'
    allowed_domains = ['zoomit.ir']
    start_urls = ['https://www.zoomit.ir/']

    # custom_settings = {
    #     'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    #     'HTTPCACHE_ENABLED': False,
    #     'ROBOTSTXT_OBEY': False, 
    # }


    def parse(self, response):
        news_links = response.css('div.bg-background2 a.sc-4c41eafb-6::attr(href)').getall()

        for link in news_links:
            if link.startswith('/'):
                link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_news)

    def parse_news(self, response):
        item = NewsItem()
        item['title'] = response.css('h1::text').get(default='').strip()
        item['content'] = ' '.join(response.css('article p::text').getall()).strip()
        item['source'] = response.url
        tags = response.css('div.sc-a11b1542-0.fCUOzW a span::text').getall()
        item['tags'] = [tag.strip() for tag in tags if tag.strip()]

        date_text = response.css('span.sc-9996cfc-0.inKOvi.fa::text').get(default='').strip()

        created_at = jalali_to_gregorian(date_text)
        item['created_at'] = created_at
            

        if item['title'] and item['content']:
            yield item



# class ZoomitSpider2(scrapy.Spider):
#     name = 'zoomit'
#     allowed_domains = ['zoomit.ir']
#     start_urls = ['https://www.zoomit.ir/']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def parse(self, response):
#         # news_links = response.css('article a::attr(href)').getall()
#         news_links = response.css('div.bg-background2 a.sc-4c41eafb-6::attr(href)').getall()

#         for link in news_links:
#             if link.startswith('/'):
#                 link = response.urljoin(link)
#             yield scrapy.Request(link, callback=self.parse_news)

#     def parse_news(self, response):
#         item = NewsItem()
#         item['title'] = response.css('h1::text').get(default='').strip()
#         item['content'] = ' '.join(response.css('article p::text').getall()).strip()
#         item['source'] = 'zoomit.ir'
#         tags = response.css('div.sc-a11b1542-0.fCUOzW a span::text').getall()
#         item['tags'] = [tag.strip() for tag in tags if tag.strip()]
        
#         if item['title'] and item['content']:
#             yield item

