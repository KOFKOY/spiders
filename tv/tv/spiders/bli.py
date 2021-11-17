import os
import re

import scrapy


class BliSpider(scrapy.Spider):
    name = 'bli'
    start_urls = ['https://biliapi.hnyoufan.com/api/app/media/m3u8/av/6o/dz/6w/gu/4bf67b7a21fa43759150df178833051a.m3u8']

    def start_requests(self):
        headers = {
            'user-agent': 'DevID%3D61ead28849d11cda%3BDevType%3Dvpro_arm64%3A25%3BSysType%3Dandroid%3BVer%3D2.0.7%3BBuildID%3Dcom.md.bili211110',
            'x-api-key': 'timestamp=1636991397;sign=48075d99b172803484253acf2f4d534cb11b79e5;nonce=5308fe43-39db-453d-b23b-2203cff5dab8',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJwdWJsaWMiLCJleHAiOjE2Mzk1ODMzNTAsImlzc3VlciI6ImNvbS5idXR0ZXJmbHkiLCJzdWIiOiJhc2lnbiIsInVzZXJJZCI6MTE3Nzk3ODl9.O9H6IFyEyKCIsWuBHghW3HKSAzP_CB-FCMmlwiT6fpc'
        }
        yield scrapy.Request(url=self.start_urls[0], headers=headers, callback=self.parse)

    def parse(self, response):
        print(response.body)
        groups = re.findall(r',(\s*.*\n*?)#', response.body.decode('utf-8'))
        g_list = list(groups)
        del g_list[0]
        for index, data in enumerate(g_list):
            yield scrapy.Request(data, callback=self.video_download, meta={'num': index})
        pass

    def video_download(self, response):
        path = '/testbli'
        if not os.path.exists(path):
            os.mkdir(path)
        num = response.meta['num']
        with open(f"{path}/{num}.ts", 'wb') as f:
            f.write(response.body)
        print('下载完成')
