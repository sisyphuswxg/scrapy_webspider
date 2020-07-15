# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    rate = scrapy.Field()
    directors = scrapy.Field()
    casts = scrapy.Field()
    type = scrapy.Field()
    runtime = scrapy.Field()
    release_date = scrapy.Field()
    imdb_link = scrapy.Field()
