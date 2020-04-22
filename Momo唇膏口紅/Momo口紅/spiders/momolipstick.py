# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import MomoItem
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class MomolipstickSpider(scrapy.Spider):
    name = 'momolipstick'
    start_urls = [
        'http://www.momomall.com.tw/s/category/1801400014/%E5%94%87%E8%86%8F/%E5%8F%A3%E7%B4%85/']
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

        next_page = 'https://www.momomall.com.tw/s/category/1801400014/4/' + \
            str(MomolipstickSpider.page) + \
            '/%E5%94%87%E8%86%8F%E5%8F%A3%E7%B4%85'
        if MomolipstickSpider.page <= 100:

            MomolipstickSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
