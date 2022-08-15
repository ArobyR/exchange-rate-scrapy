# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RateItem(scrapy.Item):
    acronym = scrapy.Field()
    rate_exchange = scrapy.Field()
    day = scrapy.Field()
    
