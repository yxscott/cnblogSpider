# coding: utf-8

import scrapy
from scrapy import Selector
from cnblogSpider.items import CnblogspiderItem

class cnblogsSpider(scrapy.Spider):

    name = 'cnblogs' # 爬虫的名称。
    allowed_domains = ['cnblogs.com']
    start_urls = [
        "https://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]

    def parse(self, response):
        papers = response.xpath("//*[@class='day']")
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url,
                                    title=title,
                                    time=time,
                                    content=content)
            request = scrapy.Request(url=url,
                                     callback=self.parse_body)
            request.meta['item'] = item
            yield request
        next_page = Selector(response).re(r'<a herf="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0],
                                 callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        print(item)
        body = response.xpath("//*[@class='postBody']")
        item['cimage_urls'] = body.xpath(".//img//@src").extract()
        yield item