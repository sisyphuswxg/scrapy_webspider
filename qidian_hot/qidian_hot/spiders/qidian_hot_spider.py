# -*-coding: utf-8-*-


from scrapy.spiders import Spider


class HotSalesSpider(Spider):
    name = 'hotsales'

    start_urls = ["https://www.qidian.com/rank/hotsales?style=1"]

    def parse(self, response):
        # xpath: book-mid-info
        list_selector = response.xpath("//div[@class='book-mid-info']")

        for one_selector in list_selector:
            # name
            name = one_selector.xpath("h4/a/text()").extract()[0]
            # author
            author = one_selector.xpath("p[1]/a[1]/text()").extract()[0]
            # type
            type = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
            # form
            form = one_selector.xpath("p[1]/span/text()").extract()[0]

            hot_dict = {
                "name": name,
                "author": author,
                "type": type,
                "form": form
            }

            yield hot_dict
