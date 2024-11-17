# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MangaItem(scrapy.Item):
    cover_art = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    latest_chapter = scrapy.Field()
    current_chapter = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()