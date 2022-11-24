# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Luxun_Book_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    book_name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    publication = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()

class Luxun_Diary_Item(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()

