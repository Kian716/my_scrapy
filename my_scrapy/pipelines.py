# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re
from openpyxl import Workbook

class MyScrapyPipeline:
    def __init__(self):
        """创建excel文件并写入标题行"""
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = '360助手App'
        self.ws.append(('名称',
                        '评分',
                        '评论数',
                        '下载量',
                        '大小',
                        '小编点评',
                        '应用简介',
                        '用户评论',
                        '爬取的评论数'))

    def close_spider(self, spider):
        """重写回调函数，在关闭爬虫时保存excel文件"""
        self.wb.save('./results.xlsx')

    def process_item(self, item, spider):
        # 对爬取的数据进行处理
        item['app_download_nums'] = re.search("([0-9]+.*)", item['app_download_nums']).group()
        intro = ''.join(item['app_intro'])
        item['app_intro'] = re.sub('\s|\t|\n', '', intro)
        item['app_crawl_review_nums'] = len(item['app_reviews'])
        item['app_reviews'] = '|\n'.join(item['app_reviews'])

        # 将数据写入excel
        self.ws.append((item['app_name'],
                        item['app_score'],
                        item['app_review_nums'],
                        item['app_download_nums'],
                        item['app_size'],
                        item['app_editor_review'],
                        item['app_intro'],
                        item['app_reviews'],
                        item['app_crawl_review_nums']))

        return item
