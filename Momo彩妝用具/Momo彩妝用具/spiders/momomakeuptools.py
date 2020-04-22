# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class MomomakeuptoolsSpider(scrapy.Spider):
    name = 'momomakeuptools'
    start_urls = [
        'https://www.momomall.com.tw/s/category/1801400020/%E5%BD%A9%E5%A6%9D%E7%94%A8%E5%85%B7%E5%88%B7%E5%85%B7/']

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
            item['product_category'] = 'MakeupTools'
            item['product_source'] = 'Momo'
            item['product_images'] = items.xpath(
                "a/img[@class='prdimg']/@src").extract()
            item['product_subcategory'] = 'makeuptools'
            if item['product_price'] != "折扣價":
                yield item

        next_page = 'https://www.momomall.com.tw/s/category/1801400020/4/' + \
            str(MomomakeuptoolsSpider.page) + \
            '/%E5%BD%A9%E5%A6%9D%E7%94%A8%E5%85%B7%E5%88%B7%E5%85%B7/'
        if MomomakeuptoolsSpider.page <= 100:

            MomomakeuptoolsSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
