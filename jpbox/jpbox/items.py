# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JpboxItem(scrapy.Item):
    jp_copies = scrapy.Field()
    jp_title = scrapy.Field()
    jp_director = scrapy.Field()
    jp_nationality = scrapy.Field()
    jp_duration = scrapy.Field()
    jp_genres = scrapy.Field()
    jp_release = scrapy.Field()
    jp_distributors = scrapy.Field()
