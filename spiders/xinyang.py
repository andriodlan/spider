import random

import scrapy
from scrapy import Spider
from scrapy_splash import SplashRequest, response
import re
from demo.items import StoreUrlItem, DazhongItem, xinyangItem
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
    name = 'xinyang'
    allowed_domains = ['www.y.soyoung.com']
    url = 'https://y.soyoung.com/hospital/s0p0l0m0i0t0a289h0o0c2'
    cookie = {'fspop': 'test', ' cy': '4', ' cye': 'guangzhou', ' _lxsdk_cuid': '176052aa6a3c8-006f512b3bfa99-c791e37-100200-176052aa6a3c8', ' _lxsdk': '176052aa6a3c8-006f512b3bfa99-c791e37-100200-176052aa6a3c8', ' _hc.v': '8e6ff90a-7d4b-803b-35db-fbb2c1067ab7.1606404450', ' s_ViewType': '10', ' _lx_utm': 'utm_source%3DBaidu%26utm_medium%3Dorganic', ' Hm_lvt_602b80cf8079ae6591966cc70a3940e7': '1606404450,1606646067,1606647183', ' lgtoken': '0fba54b0a-de54-4d27-9b9a-1a039e657fe1', ' dplet': 'd410a978792edb05bc1112d67be0c193', ' dper': '88b73a39dc1e46b729bf138e78f650f58b1659f6eba02c249f3eb5f0d8326435182c8385f6126dfffa2d1c93adbe7113edb274a0f327099d6a1f2d016e6722aedb618444deab7d333f2faf101fe2225386322f37f5b13a09905c5aece6af2b18', ' ll': '7fd06e815b796be3df069dec7836c3df', ' ua': 'dpuser_3993331742', ' ctu': '37fe8d5e14a7b493d5f548102549388a9fdaea4a572a23866190b827c070f56d', ' Hm_lpvt_602b80cf8079ae6591966cc70a3940e7': '1606647833', ' _lxsdk_s': '17613916aee-495-086-b66%7C%7C163'}

    # start request
    def start_requests(self):
        yield SplashRequest(self.url, callback=self.parse_page,args = {'lua_source': script}, endpoint='execute',dont_filter=True)

    #args = {'lua_source': script, 'wait': 0.5, 'images': 0, 'viewport': '1024x2480', 'timeout': 3600},
    # parse the html content
    def parse_page(self, response):

        page = 1
        temp = re.split("/",response.urljoin(""))[4]
        print(temp)
        for page in range(1,3):
            url = response.urljoin("/hospital/"+temp+"/"+"page/"+str(page))
            print(url)
            yield SplashRequest(url, callback=self.parse_url, dont_filter=True,
                                args={'lua_source': script, 'wait': 0.5})
    def parse_url(self, response):
        urls = response.xpath("//a[@class='pic']/@href").extract()
        temp = re.split("/", response.urljoin(""))[4]
        print(urls)
        for url in  urls:
            url = "https://y.soyoung.com"+url
            print(url)
            #https://y.soyoung.com/hospital/s0p0l0m0i0t0a289h0o0c2/
            yield SplashRequest(url, callback=self.parse_content_url,dont_filter=True,args={'lua_source': script,'wait': 0.5})
         #hhtml/body/div[4]/div[2]/ul[2]/li/a

    def parse_content_url(self, response):
            url = response.xpath(".//*[@id='bd']/div[2]/div[1]/a/@href")
            main_url = "https://y.soyoung.com"
            yield SplashRequest(main_url + url, callback=self.parse_content,dont_filter=True,args={'lua_source': script,'wait': 0.5},mete={url:main_url + url})
         #hhtml/body/div[4]/div[2]/ul[2]/li/a

    def parse_content(self, response):
            url = response.meta["url"]
            for i in range(1,5):
                 yield SplashRequest(url, callback=self.parse,dont_filter=True,args={'lua_source': script,'wait': 0.5})

    def parse(self,response):
        xinyang = xinyangItem()
        for sel in response.xpath('.//*[@id="bd"]/div[1]/div[3]/ul/li'):
            temp = re.split("/",response.urljoin(""))
            if temp[4] == "s0p0l0m0i0t0a289h0o0c2":
               xinyang['city '] = "广州"
            else:
               xinyang['city '] = "深圳"
            xinyang['level']="xinyang"
            xinyang['shop_name'] = response.xpath('.//*[@id="hd"]/div[4]/div[2]/a[1]/text()').extract()
            xinyang['price'] = sel.xpath('/p/span[@class="num"]/text()').extract()
            xinyang['title']  =  sel.xpath('/p/a/text()').extract()
            xinyang['product__appointment'] = response.xpath('/div/div[1]/span/text()').extract_first()
            xinyang['sale'] = sel.xpath('/div/div[2]/span/text()').extract_first()
           # xinyang['comment'] = str(sel.xpath('text()').extract()[3]).strip()
            yield  xinyang







