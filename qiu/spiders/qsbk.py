# -*- coding: utf-8 -*-
import scrapy
from  qiu.items import QiuItem

class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self,response):
        divs = response.xpath("//div[@id = 'content-left']/div")
        for div in divs:
            name = div.xpath(".//div[@class = 'author clearfix']/a[2]/h2/text()").get()
            if name:
                name = name.split()
            else:
                name =div.xpath(".//div[@class = 'author clearfix']/span[2]/h2/text()").get().split()
            funny = div.xpath(".//div[@class='stats']/span[1]/i/text()").get()
            comment = div.xpath(".//div[@class='stats']/span[2]/a/i/text()").get()
            img = div.xpath(".//div[@class = 'author clearfix']/a[1]/img/@src").get()
            next_url = div.xpath(".//a[@class='contentHerf']/@href").get()
            url_model = response.url.split("/text")
            url = url_model[0] +next_url
            # 跳转到详情页面
            yield scrapy.Request(
                url=url,
                callback=self.parse_detal,
                meta={"info":(name,funny,comment,img)}
            )
        #获取下一页地址
        next_page = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()



        #跳转到下一页
        if next_page:
            next_page_url = "https://www.qiushibaike.com" + next_page
        else:
            pass
        print(next_page_url)
        yield scrapy.Request(
            url=next_page_url,
            callback=self.parse,
        )


    def parse_detal(self,response):
        name,funny,comment,img = response.meta.get("info")
        content = "".join(response.xpath("//div[@class='content']/text()").getall())
        item = QiuItem(name=name,funny=funny,comment=comment,img=img,content=content)
        yield item

