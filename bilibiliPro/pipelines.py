# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import csv
import scrapy
import logging
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

logger = logging.getLogger(__name__)


class UserinfoPipeline:
    def open_spider(self, spider):
        print('start write user_info...')
        self.fp = open('./user_info.csv', 'a', newline='', encoding='utf-8')
        self.fieldnames = [
            'mid',
            'name',
            'sex',
            'face',
            'sign',
            'level',
            'following',
            'follower',
            'archive_view',
            'article_view',
            'likes',
        ]
        self.writer = csv.DictWriter(self.fp, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if item.__class__.__name__ == 'Userinfo_1Item':
            self.writer.writerow({
                'mid': item['mid'],
                'name': item['name'],
                'sex': item['sex'],
                'face': item['face'],
                'sign': item['sign'],
                'level': item['level'],
            })
            logger.warning(item)

        if item.__class__.__name__ == 'Userinfo_2Item':
            self.writer.writerow({
                'mid': item['mid'],
                'following': item['following'],
                'follower': item['follower'],
            })
            logger.warning(item)
        if item.__class__.__name__ == 'Userinfo_3Item':
            self.writer.writerow({
                'mid': item['mid'],
                'archive_view': item['archive_view'],
                'article_view': item['article_view'],
                'likes': item['likes'],
            })
            logger.warning(item)
        return item

    def close_spider(self, spider):
        print('finish write user_info...')
        self.fp.close()


class UserinfoPicsPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.__class__.__name__ == 'Userinfo_1Item' and item['face']:
            yield scrapy.Request(item['face'], headers=item['headers'])

    def file_path(self, request, response=None, info=None, *, item):
        if item.__class__.__name__ == 'Userinfo_1Item':
            fileName = str(item['mid']) + item['face'][-4:]
            print(f'{fileName} downloading...')
            return fileName

    def item_complete(self, results, item, info):
        # 返回给下个即将执行的管道类
        logger.warning(item)
        return item
