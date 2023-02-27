from urllib.parse import urljoin

import scrapy
from scrapy import Request

from my_scrapy.items import App


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['zhushou.360.cn']
    start_urls = ['https://zhushou.360.cn/list/index/cid/102139/']

    def start_requests(self):
        """将所有的App列表页加入请求列表"""
        for page in range(11):
            yield Request('https://zhushou.360.cn/list/index/cid/102139/?page={}'.format(page+1))

    def parse(self, response):
        """解析App列表页"""
        list_items = response.xpath('//ul[@id="iconList"]/li')
        for list_item in list_items:
            app = App()
            app['app_name'] = list_item.xpath('h3/a/text()').extract_first()
            # App详情页
            detail_url = urljoin('https://zhushou.360.cn', list_item.xpath('a[1]/@href').extract_first())
            # 将App详情页传给Request，并调用回调函数(被另一个函数所调用的函数)来对App详情页进行解析，同时传入回调函数参数(App对象)
            yield Request(url=detail_url,
                          callback=self.parse_detail,
                          cb_kwargs={'app': app})

    def parse_detail(self, response, **kwargs):
        """解析App详情页"""
        app = kwargs['app']
        app['app_score'] = response.xpath('//*[@id="app-info-panel"]//div[@class="pf els"]/span[1]/text()').extract_first()
        app['app_review_nums'] = response.xpath('//*[@id="comment-num"]/span/text()').extract_first()
        app['app_download_nums'] = response.xpath('//*[@id="app-info-panel"]//div[@class="pf els"]/span[3]/text()').extract_first()
        app['app_size'] = response.xpath('//*[@id="app-info-panel"]//div[@class="pf els"]/span[4]/text()').extract_first()
        app['app_editor_review'] = response.xpath('//*[@id="app-info-panel"]/div/dl/dd/p/text()').extract_first()
        app['app_intro'] = response.xpath('//*[@id="sdesc"]/div//text()').extract()
        app['app_reviews'] = response.xpath('//*[@id="review-panel"]//li/div/p[1]/span[2]/text()').extract()
        yield app



