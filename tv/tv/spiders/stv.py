import re

import scrapy


class StvSpider(scrapy.Spider):
    name = 'stv'
    start_urls = ['http://91kanju2.com/vod-play/61071-1-1.html']

    def parse(self, response):
        # with open("test.html",'w',encoding='utf-8') as f:
        #     f.write(response.body.decode('utf-8'))
        groups = re.search('https://(\S)*.m3u8', response.body.decode('utf-8'))
        print(groups.group())
        yield scrapy.Request(groups.group(), callback=self.video_detail)

    def video_detail(self, response):
        with open("test.html", 'wb') as f:
            f.write(response.body)
        groups = re.findall(r',(\s*.*\n*?)#', response.body.decode('utf-8'))
        g_list = list(groups)
        for index, data in enumerate(g_list):
            yield scrapy.Request(data, callback=self.video_download, meta={'num': index})

    def video_download(self, response):
        num = response.meta['num']
        with open(f"{num}.ts", 'wb') as f:
            f.write(response.body)
        print('下载完成')
