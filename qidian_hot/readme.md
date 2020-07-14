

* run
```bash
➜ scrapy crawl hotsales -o hot.csv 
```
其中，hotsales是爬虫定义的名字，参见./spiders/qidian_hot_spider.py::HotSalesSpider中的name属性
爬虫执行完后，数据会自动保存到hot.csv文件