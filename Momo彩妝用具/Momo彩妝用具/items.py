# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MomoItem(scrapy.Item):
    product_images = scrapy.Field()
    product_source = scrapy.Field()
    product_category = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_subcategory = scrapy.Field()
