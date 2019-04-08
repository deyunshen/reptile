# -*- coding: utf-8 -*-
import scrapy

from reptile.items import reptileItem


class ReptileSpiderSpider(scrapy.Spider):
    #爬虫名
    name = 'reptile_spider'
    #允许的域名
    allowed_domains = ['movie.reptile.com']
    #入口url 扔到调度器里面
    start_urls = ['xxxx']

    def parse(self, response):
        movie_list=response.xpath("//*[@id='content']/div/div[1]/ol/li")
        for i_item in movie_list:
            douban_item=reptileItem()
            douban_item['serial_number']=i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            content=i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s= "".join(i_content.split())
                douban_item['introduce']=content_s
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='evaluate']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            yield  douban_item
        next_link=response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.reptile.com/"+next_link,callback=self.parse)