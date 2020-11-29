import random

import scrapy
from scrapy import Spider
from scrapy_splash import SplashRequest, response
import re
from demo.items import StoreUrlItem,  DazhongItem
from demo.settings import USER_AGENT_LIST

script = """
         
            function main(splash, args)
              splash.js_enabled = true
              splash.resource_timeout = 20
              splash.images_enabled = false
              assert(splash:go(args.url))
              assert(splash:wait(0.5))
              return { html = splash:html()}
            end
         """


class dazhongSpider(Spider):
    name = 'dazhong'
    allowed_domains = ['www.dianping.com']
    url = 'http://www.dianping.com/guangzhou/ch85/g183'
    cookie = {'fspop': 'test', ' cy': '4', ' cye': 'guangzhou', ' _lxsdk_cuid': '176052aa6a3c8-006f512b3bfa99-c791e37-100200-176052aa6a3c8', ' _lxsdk': '176052aa6a3c8-006f512b3bfa99-c791e37-100200-176052aa6a3c8', ' _hc.v': '8e6ff90a-7d4b-803b-35db-fbb2c1067ab7.1606404450', ' s_ViewType': '10', ' _lx_utm': 'utm_source%3DBaidu%26utm_medium%3Dorganic', ' Hm_lvt_602b80cf8079ae6591966cc70a3940e7': '1606404450,1606646067,1606647183', ' lgtoken': '0fba54b0a-de54-4d27-9b9a-1a039e657fe1', ' dplet': 'd410a978792edb05bc1112d67be0c193', ' dper': '88b73a39dc1e46b729bf138e78f650f58b1659f6eba02c249f3eb5f0d8326435182c8385f6126dfffa2d1c93adbe7113edb274a0f327099d6a1f2d016e6722aedb618444deab7d333f2faf101fe2225386322f37f5b13a09905c5aece6af2b18', ' ll': '7fd06e815b796be3df069dec7836c3df', ' ua': 'dpuser_3993331742', ' ctu': '37fe8d5e14a7b493d5f548102549388a9fdaea4a572a23866190b827c070f56d', ' Hm_lpvt_602b80cf8079ae6591966cc70a3940e7': '1606647833', ' _lxsdk_s': '17613916aee-495-086-b66%7C%7C163'}

    # start request
    def start_requests(self):

        yield SplashRequest(self.url, callback=self.parse_url, endpoint='execute',args={'lua_source': script,'wait': 0.5,'images': 0,'viewport': '1024x2480','timeout': 3600},dont_filter=True)

    # parse the html content
    def parse_url(self, response):
        urls = response.xpath(".//*[@id='shop-all-list']/ul/li/div/div[@class='tit']/a/@href").extract()
        for url  in  urls:
            yield SplashRequest(url, callback=self.parse,dont_filter=True,args={'lua_source': script,'wait': 0.5,'images': 0,'viewport': '1024x2480','timeout': 3600})

    def parse(self,response):
        dazhongitem = DazhongItem()
        for sel in response.xpath('.//*[@id="sales"]/div[2]/a'):
            dazhongitem['shop_name'] = response.xpath('.//*[@id="basic-info"]/h1/text()').extract_first()
            dazhongitem['price'] = sel.xpath('span/text()').extract_first()
            dazhongitem['title']  =  str(sel.xpath('text()').extract()[3]).strip()
            yield  dazhongitem






