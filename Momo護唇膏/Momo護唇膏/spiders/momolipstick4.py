# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Momolipstick4Spider(scrapy.Spider):
    name = 'momolipstick4'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400017/%E8%AD%B7%E5%94%87%E8%86%8F/']

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
            item['product_subcategory'] = 'otherlipstick'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400017/4/' + \
            str(Momolipstick4Spider.page) + '/%E8%AD%B7%E5%94%87%E8%86%8F/'
        if Momolipstick4Spider.page <= 100:

            Momolipstick4Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
