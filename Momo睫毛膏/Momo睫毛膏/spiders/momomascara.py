# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class MomomascaraSpider(scrapy.Spider):
    name = 'momomascara'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400013/%E7%9D%AB%E6%AF%9B%E8%86%8F/']

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
            item['product_category'] = 'Mascara'
            item['product_source'] = 'Momo'
            item['product_images'] = items.xpath(
                "a/img[@class='prdimg']/@src").extract()
            item['product_subcategory'] = 'mascara'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400013/4/' + \
            str(MomomascaraSpider.page) + '/%E7%9D%AB%E6%AF%9B%E8%86%8F/'
        if MomomascaraSpider.page <= 100:

            MomomascaraSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
