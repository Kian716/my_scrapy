# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class App(Item):
    app_name = Field()
    app_score = Field()
    app_review_nums = Field()
    app_download_nums = Field()
    app_size = Field()
    app_editor_review = Field()
    app_intro = Field()
    app_review = Field()


