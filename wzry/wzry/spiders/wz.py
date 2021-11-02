import scrapy

from wzry.items import WzryItem


class WzSpider(scrapy.Spider):
    name = 'wz'
    start_urls = ['https://pvp.qq.com/web201605/herolist.shtml']

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
        hero_list = response.xpath("//ul[@class='herolist clearfix']/li/a/@href").getall()
        print(f'英雄个数{len(hero_list)}')
        for hero_url in hero_list:
            yield scrapy.Request(response.urljoin(hero_url), callback=self.parse_hero_deatil)
