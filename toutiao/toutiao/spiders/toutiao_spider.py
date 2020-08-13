# -*-coding: utf-8-*-


from scrapy.spiders import Spider, Request
from selenium import webdriver
from toutiao.items import ToutiaoItem


class ToutiaoSpider(Spider):
    name = 'toutiao'

    def __init__(self):
        # self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Firefox()

    def start_requests(self):
        url = "https://toutiao.com/ch/news_hot/"
        yield Request(url)

    def parse(self, response):
        item = ToutiaoItem()
        list_selectors = response.xpath("//div[@class='wcommonFeed']/ul/li")
        for li in list_selectors:
            try:
                title = li.xpath(".//a[@class='link title']/text()").extract()
                title = title[0].strip(" ")
                print("title:", title)
                source = li.xpath(".//a[@class='lbtn source']/text()").extract()
                source = source[0].strip("⋅").strip(" ")
                print("source:", source)
                comment = li.xpath(".//a[@class='lbtn comment']/text()")
                comment = comment.re("(.*?)评论")[0]
                comment = "".join(comment.split())
                print("comment:", comment)

                item['title'] = title
                item['source'] = source
                item['comment'] = comment
                yield item
            except:
                continue
