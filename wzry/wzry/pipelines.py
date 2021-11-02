# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class WzryPipeline(ImagesPipeline):
    def open_spider(self, spider):
        print("开始爬虫")

    def get_media_requests(self, item, info):
        images = item['images']
        for image_url in images:
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.url.split('/')[-1]
        return item['name']+"/" + image_name

    def item_completed(self, results, item, info):
        return item

    def close_spider(self, spider):
        print('结束爬虫')
