# -*-coding: utf-8-*-


from scrapy.spiders import Spider, Request
from qq_music.items import QqMusicItem

import json


class MusicSpider(Spider):
    name = 'music'

    def start_requests(self):
        # why this url??
        url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?&topid=4"
        yield Request(url)

    def parse(self, response):
        item = QqMusicItem()
        json_text = response.text
        music_dict = json.loads(json_text)
        for one_music in music_dict["songlist"]:
            item["song_name"] = one_music["data"]["songname"]
            item["album_name"] = one_music["data"]["albumname"]
            item["singer_name"] = one_music["data"]["singer"][0]["name"]
            item["interval_name"] = one_music["data"]["interval"]

            yield item

