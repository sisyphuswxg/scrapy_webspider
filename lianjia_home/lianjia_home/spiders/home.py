# -*- coding: utf-8 -*-
import scrapy

from scrapy import Request
from lianjia_home.items import LianjiaHomeItem


class HomeSpider(scrapy.Spider):
    name = 'home'
    current_page = 1
    total_page = 100
    # allowed_domains = ['https://sz.lianjia.com/ershoufang/']
    # start_urls = ['http://https://sz.lianjia.com/ershoufang//']

    def start_requests(self):
        url = "https://sz.lianjia.com/ershoufang/"
        yield Request(url)

    def parse(self, response):
        selectors = response.xpath("//li/div[@class='info clear']")
        for selector in selectors:
            try:
                name = selector.xpath("div [@class='flood']/div [@class='positionInfo']/a/text()").extract()[0]

                # get other info
                other = selector.xpath("div [@class='address']/div [@class='houseInfo']/text()").extract()[0]
                other_list = other.split('|')
                type = other_list[0].strip(" ")
                area = other_list[1].strip(" ")
                direction = other_list[2].strip(" ")
                fitment = other_list[3].strip(" ")
                elevator = "TODO"

                # get price info
                total_price = selector.xpath("div [@class='priceInfo']/div [@class='totalPrice']/span/text()").extract()[0]
                unit_price = selector.xpath("div [@class='priceInfo']/div [@class='unitPrice']/span/text()").extract()[0]

                item = LianjiaHomeItem()
                item['name'] = name
                item['type'] = type
                item['area'] = area
                item['direction'] = direction
                item['fitment'] = fitment
                # item['elevator'] = elevator
                item['total_price'] = total_price
                item['unit_price'] = unit_price

                # in detail info
                # get url
                detail_url = selector.xpath("div [@class='title']/a/@href").extract()[0]
                yield Request(detail_url,
                              meta={"item": item},
                              callback=self.detail_parse)
            except:
                pass

            # more page
            self.current_page += 1
            if self.current_page <= self.total_page:
                next_url = "https://sz.lianjia.com/ershoufang/pg%d" % self.current_page
                yield Request(next_url)

    def detail_parse(self, response):
        elevator = response.xpath("//div [@class='base']/div [@class='content']/ul/li[11]/text()").extract()[0]
        property = response.xpath("//div [@class='transaction']/div [@class='content']/ul/li[6]/span[2]/text()").extract()[0]

        item = response.meta['item']
        item['elevator'] = elevator
        item['property'] = property
        yield item

