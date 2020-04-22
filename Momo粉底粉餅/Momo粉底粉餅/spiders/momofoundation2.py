# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Momofoundation2Spider(scrapy.Spider):
    name = 'momofoundation2'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400003/%E7%B2%89%E5%BA%95/%E7%B2%89%E9%A4%85/']

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
            item['product_subcategory'] = 'pressedpowder'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400003/4/' + \
            str(Momofoundation2Spider.page) + \
            '/%E7%B2%89%E5%BA%95/%E7%B2%89%E9%A4%85/'
        if Momofoundation2Spider.page <= 100:

            Momofoundation2Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
