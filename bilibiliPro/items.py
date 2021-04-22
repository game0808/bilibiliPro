# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Userinfo_1Item(scrapy.Item):
    mid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    face = scrapy.Field()
    sign = scrapy.Field()
    level = scrapy.Field()
    headers = scrapy.Field()


class Userinfo_2Item(scrapy.Item):
    mid = scrapy.Field()
    following = scrapy.Field()
    follower = scrapy.Field()


class Userinfo_3Item(scrapy.Item):
    mid = scrapy.Field()
    archive_view = scrapy.Field()
    article_view = scrapy.Field()
    likes = scrapy.Field()
