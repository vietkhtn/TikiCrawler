# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TikiProductInfo(scrapy.Item):
    productID = scrapy.Field()
    productSKU = scrapy.Field()
    productName = scrapy.Field()
    productPrice = scrapy.Field()
    productDescription = scrapy.Field()
    productCategory = scrapy.Field()

class TikiUserRating(scrapy.Item):
    stt = scrapy.Field()
    userRate = scrapy.Field()
    productRate = scrapy.Field()
    timeRate =scrapy.Field()
    starRate = scrapy.Field()
    commentRate = scrapy.Field()