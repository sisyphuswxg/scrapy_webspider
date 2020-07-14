# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QqMusicItem(scrapy.Item):
    # define the fields for your item here like:
    song_name = scrapy.Field()
    album_name = scrapy.Field()
    singer_name = scrapy.Field()
    interval_name = scrapy.Field()
