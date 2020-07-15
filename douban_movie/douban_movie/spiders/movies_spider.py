# -*-coding: utf-8-*-


from scrapy.spiders import Spider, Request

from douban_movie.items import DoubanMovieItem

import json


class MoviesSpider(Spider):
    name = 'movies'

    current_page = 1

    def start_requests(self):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=rank&page_limit=20&page_start=0'
        yield Request(url=url, dont_filter=True)

    def parse(self, response):
        item = DoubanMovieItem()
        json_text = response.text
        movie_dict = json.loads(json_text)

        for one_movie in movie_dict["subjects"]:
            item["title"] = one_movie["title"]
            item["rate"] = one_movie["rate"]
            yield item

            # # directors,
            # target_url = one_movie["url"]
            # yield Request(url=target_url,
            #               meta={"item": item},
            #               dont_filter=True,
            #               callback=self.target_one_parse,
            #               )

        # if self.current_page <= 25:
        #     url_next = f"https://movie.douban.com/j/search_subjects?type=movie&tag=经典&sort=rank&page_limit=20&page_start={self.current_page * 20}"
        #     self.current_page += 1
        #     yield Request(url_next)

    def target_one_parse(self, response):
        directors = response.xpath("//div [@class='subject clearfix']/div [@id='info']/span[1]/span[2]/a/text()").extract()[0]

        actors = response.xpath("//div [@class='subject clearfix']/div [@id='info']/span[3]/span[2]/a/text()").extract()
        # get First three actors
        actors_str = actors[0].strip() + ", " + actors[2].strip() + ", " + actors[2].strip()

        type = response.xpath("//div [@class='subject clearfix']/div [@id='info']/span [@property='v:genre']/text()").extract()
        type = ",".join(type)

        runtime = response.xpath("//div [@class='subject clearfix']/div [@id='info']/span [@property='v:runtime']/text()").extract()[0]
        release_date = response.xpath("//div [@class='subject clearfix']/div [@id='info']/span [@property='v:initialReleaseDate']/text()").extract()
        release_date = ",".join(release_date)
        imdb_link = response.xpath("//div [@class='subject clearfix']/div [@id='info']/a/@href").extract()[0]

        item = response.meta['item']
        item['directors'] = directors
        item['casts'] = actors_str
        item['type'] = type
        item['runtime'] = runtime
        item['release_date'] = release_date
        item['imdb_link'] = imdb_link
        yield item
