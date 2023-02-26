from urllib.parse import urljoin

import scrapy
from scrapy import Request
from my_scrapy.middlewares import MyScrapyDownloaderMiddleware

from my_scrapy.items import App
from my_scrapy.utils import create_my_webdiver

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['zhushou.360.cn']
    start_urls = ['http://zhushou.360.cn/list/index/cid/102139/']

    def start_requests(self):
        for page in range(1):
            yield Request('https://zhushou.360.cn/list/index/cid/102139/?page={}'.format(page+1))


    def parse(self, response):
        list_items = response.xpath('//ul[@id="iconList"]/li')
        for list_item in list_items:
            app = App()
            app['app_name'] = list_item.xpath('h3/a/text()').extract()
            detail_url = urljoin('http://zhushou.360.cn', list_item.xpath('a[1]/@href').extract_first())
            yield Request(url=detail_url,
                          callback=self.parse_detail,
                          cb_kwargs={'app': app})

    def parse_detail(self, response, **kwargs):
        app = kwargs['app']
        app['app_score'] = response.xpath('//*[@id="app-info-panel"]//div[@class="pf els"]/span[1]/text()').extract_first()
        app['app_review_nums'] = response.xpath('//*[@id="comment-num"]/span/text()').extract_first()
        app['app_download_nums'] = response.xpath('//*[@id="app-info-panel"]//div[@class="pf els"]/span[3]/text()').extract_first()
        app['app_size'] = response.xpath('//*[@id="app-info-panel"]//div[@class="pf els"]/span[4]/text()').extract_first()
        app['app_editor_review'] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/p/text()').extract_first()
        # app['app_intro'] = response.xpath('//*[@id="sdesc"]/div//text()').extract()
        app['app_review'] = response.xpath('//*[@id="review-panel"]/li[1]/div/p[1]/span[2]/text()').extract()
        yield app



