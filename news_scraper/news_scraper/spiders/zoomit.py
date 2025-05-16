# import scrapy


# class ZoomitSpider(scrapy.Spider):
#     name = "zoomit"
#     allowed_domains = ["zoomit.ir"]
#     start_urls = ["https://zoomit.ir"]

#     def parse(self, response):
#         pass

import scrapy
from ..items import NewsItem

class ZoomitSpider(scrapy.Spider):
    name = 'zoomit'
    allowed_domains = ['zoomit.ir']
    start_urls = ['https://www.zoomit.ir/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        news_links = response.css('article a::attr(href)').getall()

        for link in news_links:
            if link.startswith('/'):
                link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_news)

    def parse_news(self, response):
        item = NewsItem()
        item['title'] = response.css('h1::text').get(default='').strip()
        item['content'] = ' '.join(response.css('article p::text').getall()).strip()
        item['source'] = 'zoomit.ir'
        tags = response.css('div.sc-a11b1542-0.fCUOzW a span::text').getall()
        item['tags'] = [tag.strip() for tag in tags if tag.strip()]
        
        if item['title'] and item['content']:
            yield item

