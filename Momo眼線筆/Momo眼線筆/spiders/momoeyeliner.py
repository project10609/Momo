# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class MomoeyelinerSpider(scrapy.Spider):
    name = 'momoeyeliner'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400010/%E7%9C%BC%E7%B7%9A%E7%AD%86/%E6%B6%B2/%E8%86%A0/']

    page = 2

    def parse(self, response):
        item = MomoItem()
        for items in response.xpath("//div[@class='prdListArea']/ul[@class='list']/li"):
            item['product_name'] = items.xpath(
                "a/p[@class='prdName']/text()").extract()
            item['product_price'] = items.xpath(
                "a/p[@class='prdPrice']/b[1]/text()").extract_first().replace(',', '')
            item['product_url'] = 'http://www.momomall.com.tw' + \
                items.xpath("a/@href").extract()[0]
            item['product_category'] = 'EyeLiner'
            item['product_source'] = 'Momo'
            item['product_images'] = items.xpath(
                "a/img[@class='prdimg']/@src").extract()
            item['product_subcategory'] = 'eyeliner'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400010/4/' + \
            str(MomoeyelinerSpider.page) + \
            '/%E7%9C%BC%E7%B7%9A%E7%AD%86/%E6%B6%B2/%E8%86%A0/'
        if MomoeyelinerSpider.page <= 100:

            MomoeyelinerSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
