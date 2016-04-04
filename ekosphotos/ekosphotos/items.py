# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EkosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    uploader = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    views = scrapy.Field()
    album = scrapy.Field()
    photo_id = scrapy.Field()
    pass
