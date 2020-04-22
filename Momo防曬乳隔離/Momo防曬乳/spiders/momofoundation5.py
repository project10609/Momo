# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Momofoundation5Spider(scrapy.Spider):
    name = 'momofoundation5'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400009/%E9%98%B2%E6%9B%AC%E4%B9%B3/%E9%9A%94%E9%9B%A2/']

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
            item['product_category'] = 'Foundation'
            item['product_source'] = 'Momo'
            item['product_images'] = items.xpath(
                "a/img[@class='prdimg']/@src").extract()
            item['product_subcategory'] = 'isolation'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400009/4/' + \
            str(Momofoundation5Spider.page) + \
            '/%E9%98%B2%E6%9B%AC%E4%B9%B3/%E9%9A%94%E9%9B%A2/'
        if Momofoundation5Spider.page <= 100:

            Momofoundation5Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
