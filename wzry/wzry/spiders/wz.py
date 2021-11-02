import json

import scrapy

from wzry.items import WzryItem


class WzSpider(scrapy.Spider):
    name = 'wz'
    # start_urls = ['https://pvp.qq.com/web201605/herolist.shtml']
    start_urls = ['https://pvp.qq.com/web201605/js/herolist.json']

    def parse_hero_deatil(self, response):
        item = WzryItem()
        name = response.xpath("//h2[@class='cover-name']/text()").get()
        item['name'] = name
        template = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'
        hero_code = response.xpath("//div[@class='zk-con1 zk-con']/@style").get().split("/")[-2]
        skin_num = len(response.xpath("//ul[@class='pic-pf-list pic-pf-list3']/@data-imgname").get().split('|')) + 1
        image_list = []
        for i in range(1, skin_num):
            image_list.append(template.format(hero_code, hero_code, i))
        item['images'] = image_list
        yield item

    def parse(self, response, **kwargs):
        heros = json.loads(response.text)
        print("开始爬虫……")
        print("英雄数量：", len(heros))
        template = 'herodetail/{}.shtml'
        base_url = 'https://pvp.qq.com/web201605/'
        test = heros[1:3]
        for item in test:
            yield scrapy.Request(base_url + template.format(item['ename']), callback=self.parse_hero_deatil)

    @staticmethod
    def close(spider, reason):
        print("爬虫完成")
