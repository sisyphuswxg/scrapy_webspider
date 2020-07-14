# -*-coding: utf-8-*-


from scrapy.spiders import Spider
from scrapy.spiders import Request
from qidian_hot_pro.items import QidianHotProItem
from scrapy.loader import ItemLoader


class HotSalesProSpider(Spider):
    name = 'hotsalespro'
    current_page = 1

    def start_requests(self):
        url = "https://www.qidian.com/rank/hotsales?style=1"

        # add custom headers: fake browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.116 Safari/537.36",
        }
        # yield Request(url, headers=headers, callback=self.css_parse)
        yield Request(url, headers=headers, callback=self.qidian_parse)

    # custom parse method
    def qidian_parse(self, response):
        # xpath: book-mid-info
        list_selector = response.xpath("//div[@class='book-mid-info']")
        for one_selector in list_selector:
            # # generate ItemLoader
            # novel = ItemLoader(item=QidianHotProItem(), selector=one_selector)
            # novel.add_xpath("name", "h4/a/text()")
            # novel.add_xpath("author", "p[1]/a[1]/text()")
            # novel.add_xpath("type", "p[1]/a[2]/text()")
            # novel.add_xpath("form", "p[1]/span/text()")
            # yield novel.load_item()

            # name
            # print(one_selector.xpath("h4/a/text()")) -> extract
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
            print(hot_dict['form'])
            yield hot_dict

            # more page
            self.current_page += 1
            if self.current_page <= 25:
                next_url = "https://www.qidian.com/rank/hotsales?style=1&page=%d" % self.current_page
                yield Request(next_url, callback=self.qidian_parse)

    '''
    # use css parse
    def css_parse(self, response):
        # css
        list_selector = response.css("[class='book-mid-info']")

        for one_selector in list_selector:
            # name
            name = one_selector.css("h4>a::text").extract()[0]
            # author
            author = one_selector.css(".author a::text").extract()[0]
            # type
            type = one_selector.css(".author a::text").extract()[1]
            # form
            form = one_selector.css(".author span::text").extract()[0]

            # hot_dict = {
            #     "name": name,
            #     "author": author,
            #     "type": type,
            #     "form": form
            # }

            # use Item
            item = QidianHotProItem()
            item['name'] = name
            item['author'] = author
            item['type'] = type
            item['form'] = form
            yield item
    '''
