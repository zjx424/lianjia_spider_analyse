# -*- coding: utf-8 -*-
import scrapy
import re
import json
import pymysql

from mysql_test import connect_config
connection=connect_config('lianjia')

class LianjiaSpider(scrapy.Spider):


    name = 'lianjia'
    def start_requests(self):
        urllist=['https://sz.lianjia.com/ershoufang/rs/','https://gz.lianjia.com/ershoufang/rs/','https://fs.lianjia.com/ershoufang/rs/','https://zh.lianjia.com/ershoufang/rs/','https://zs.lianjia.com/ershoufang/rs/','https://hui.lianjia.com/ershoufang/rs/']
        for url in urllist:
            yield scrapy.Request(url)

    def parse(self, response):
        city=re.findall("https://(.*?)\.",response.url)[0]

        rl = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        urls = ["https://{}.lianjia.com".format(city) + i for i in rl]
        for url in urls:
            yield scrapy.Request(url, callback=self.get_region)

    def get_region(self,response):
        rl = response.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href').extract()
        first_url = re.findall('((.*?)com)', response.url)[0][0]
        urllist = [first_url + i for i in rl]
        for url in urllist:
            yield scrapy.Request(url, callback=self.parse_url)

    def parse_url(self, response):
        urllist = []
        if response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data') != []:
            next_page = json.loads(
                response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0])
            totalPage = next_page["totalPage"]
            if totalPage != None:
                for i in range(1, totalPage + 1):
                    urllist.append(response.url + "pg{}".format(i))
            for url in urllist:
                yield scrapy.Request(url, callback=self.get_item)

    def get_item(self, response):

        item = {}
        detail_urls = response.xpath('//div[@class="info clear"]//div[@class="title"]/a/@href').extract()
        titles = response.xpath('//div[@class="info clear"]//div[@class="title"]/a/text()').extract()
        times = response.xpath('//div[@class="followInfo"]//text()').extract()
        addresses = response.xpath('//div[@class="address"]//a/text()').extract()
        total_prices = response.xpath('//div[@class="totalPrice"]/span/text()').extract()
        unit_Prices = response.xpath('//div[@class="unitPrice"]/span/text()').extract()

        for title, time, detail_url, address, total_price, unit_Price in zip(titles, times, detail_urls,
                                                                                   addresses, total_prices,
                                                                                   unit_Prices):
            unit_Price = re.findall('(\d+)', unit_Price)[0]
            total_price = re.findall('(\d+)', total_price)[0]



            item["title"] = title
            item["address"] = address
            item['followinfo']=time
            item["url"] = detail_url
            item["unit_Price"] = unit_Price
            item["total_price"] = total_price
            yield scrapy.Request(item["url"], callback=self.parse_detail, meta={'item': item})


    def parse_detail(self, response):
        item = response.meta['item']

        area=response.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()').extract()[0] if len(response.xpath('//div[@class="area"]/div[@class="mainInfo"]').extract())!=0 else None
        area1 = response.xpath('//div[@class="areaName"]/span/a[1]/text()').extract()[0] if len(
            response.xpath('//div[@class="areaName"]/span/a[1]/text()').extract()) != 0 else None
        area2 = response.xpath('//div[@class="areaName"]/span/a[2]/text()').extract()[0] if len(
            response.xpath('//div[@class="areaName"]/span/a[2]/text()').extract()) != 0 else None
        room=response.xpath('//div[@class="base"]//li[1]/text()').extract()[0]  if len(response.xpath('//div[@class="base"]//li[1]/text()').extract())!= 0 else None
        floor=response.xpath('//div[@class="base"]//li[2]/text()').extract()[0] if len(response.xpath('//div[@class="base"]//li[2]/text()').extract())!= 0 else None
        direction=response.xpath('//div[@class="type"]/div[@class="mainInfo"]/text()').extract()[0] if len(response.xpath('//div[@class="type"]/div[@class="mainInfo"]/text()').extract())!= 0 else None
        type=response.xpath('//div[@class="transaction"]//li[2]/span[2]/text()').extract()[0] if len(response.xpath('//div[@class="transaction"]//li[2]/span[2]/text()').extract())!= 0 else None
        recommend=response.xpath('//div[@class="title"]//div[@class="sub"]/text()').extract()[0] if len(response.xpath('//div[@class="title"]//div[@class="sub"]/text()').extract())!= 0 else None


        item["area"]=area
        item["area1"] = area1
        item["area2"] = area2
        item['room']=room
        item['floor']=floor
        item['direction']=direction
        item["type"]=type
        item['recommend']=recommend
        city = re.findall("https://(.*?)\.", item["url"])[0]

        insert_table_sql = """\
        INSERT INTO %s(title,address,followinfo,url,unit_Price,total_price,area,area1,area2,room,floor,direction,type,recommend)
         VALUES('{title}','{address}', '{followinfo}', '{url}', '{unit_Price}', '{total_price}', '{area}', '{area1}', '{area2}', '{room}', '{floor}', '{direction}', '{type}', '{recommend}')
        """ % city
        with connection.cursor() as cursor:
            cursor.execute(insert_table_sql.format(title=item['title'],address=item['address'],followinfo=item['followinfo'],url=item['url'],unit_Price=item['unit_Price'],total_price=item['total_price'],area=item['area'],area1=item['area1'],area2=item['area2'],room=item['room'],floor=item['floor'],direction=item['direction'],type=item['type'],recommend=item['recommend']))
            connection.commit()

        ###linux后台执行程序的语句:
            #nohup python -u test.py > test.log 2>&1 &



