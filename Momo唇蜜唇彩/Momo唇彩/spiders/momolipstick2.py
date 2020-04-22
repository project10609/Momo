# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Momolipstick2Spider(scrapy.Spider):
    name = 'momolipstick2'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400015/4/1/%E5%94%87%E5%BD%A9%E5%94%87%E8%9C%9C/']
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
            item['product_category'] = 'Lipstick'
            item['product_source'] = 'Momo'
            item['product_images'] = items.xpath(
                "a/img[@class='prdimg']/@src").extract()
            item['product_subcategory'] = 'LipstickSub'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400015/4/' + \
            str(Momolipstick2Spider.page) + \
            '/%E5%94%87%E5%BD%A9%E5%94%87%E8%9C%9C/'
        if Momolipstick2Spider.page <= 100:

            Momolipstick2Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
