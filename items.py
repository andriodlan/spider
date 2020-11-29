# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DazhongItem(scrapy.Item):
    shop_name = scrapy.Field()
    price  = scrapy.Field()
    title = scrapy.Field()


class StoreUrlItem(scrapy.Item):

    storeUrl  = scrapy.Field()
