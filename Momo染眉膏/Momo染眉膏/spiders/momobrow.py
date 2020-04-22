# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class MomobrowSpider(scrapy.Spider):
    name = 'momobrow'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400012/%E6%9F%93%E7%9C%89%E8%86%8F/%E7%9C%89%E7%AD%86/%E7%9C%89%E7%B2%89/']

    page = 2

    def parse(self, response):
        item = MomoItem()
        for items in response.xpath("//div[@class='prdListArea']/ul[@class='list']/li"):
            item['product_name'] = items.xpath(
                "a/p[@class='prdName']/text()").extract()
            item['product_price'] = items.xpath(
                "a/p[@class='prdPrice']/b/text()").extract_first().replace(',', '')
            item['product_url'] = 'http://www.momomall.com.tw' + \
                items.xpath("a/@href").extract()[0]
            item['product_category'] = 'Brow'
            item['product_source'] = 'Momo'
            item['product_images'] = items.xpath(
                "a/img[@class='prdimg']/@src").extract()
            item['product_subcategory'] = 'brow'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400012/4/' + \
            str(MomobrowSpider.page) + \
            '/%E6%9F%93%E7%9C%89%E8%86%8F/%E7%9C%89%E7%AD%86/%E7%9C%89%E7%B2%89/'
        if MomobrowSpider.page <= 100:

            MomobrowSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
