# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class App(Item):
    # app名称
    app_name = Field()
    # app评分
    app_score = Field()
    # app评论数
    app_review_nums = Field()
    # app下载量
    app_download_nums = Field()
    # app大小
    app_size = Field()
    # app小编点评
    app_editor_review = Field()
    # app简介
    app_intro = Field()
    # app评论(用"|\n"分隔不同用户的评论)
    app_reviews = Field()
    # 爬取的评论数
    app_crawl_review_nums = Field()


