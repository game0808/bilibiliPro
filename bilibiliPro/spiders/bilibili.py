import json
import scrapy
import logging
import requests
from ..items import *
from time import sleep
import random
from fake_useragent import UserAgent


logger = logging.getLogger(__name__)
ua = UserAgent()


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # 据观察uid不是顺序分布，目前最多到703222999，大多是僵尸号
    uid = 0
    start_uid = 1
    end_uid = 10000
    # 设置cookie
    my_cookie = "SESSDATA=; bili_jct=;"

    start_urls = ['https://space.bilibili.com/' + str(start_uid)]

    def parse(self, response):
        for i in range(self.start_uid, self.end_uid):
            self.uid = i
            headers = {
                'User-Agent': ua.random,
                'referer': 'https://space.bilibili.com/' + str(self.uid),
                'origin': 'https://space.bilibili.com',
                'cookie': self.my_cookie,
            }
            new_url = 'https://api.bilibili.com/x/space/acc/info?mid=' + \
                str(self.uid) + '&jsonp=jsonp'
            sleep(random.uniform(1.0, 3.0))
            try:
                yield scrapy.Request(url=new_url, headers=headers, meta={'uid': self.uid, 'headers': headers}, callback=self.user_info_parse)
            except:
                logger.error(new_url)

    def user_info_parse(self, response):
        # 如果被封禁ip，停止爬虫，可使用代理继续
        if response.status == 412:
            self.crawler.engine.close_spider(self, '412,停止运行')
        # 正常响应，进行解析
        user_info_1 = json.loads(response.text)
        user_info_1_item = Userinfo_1Item()
        response_uid = str(response.meta['uid'])
        headers = response.meta['headers']
        # 遇到空号则记录下uid，跳过其他信息获取
        if user_info_1['code'] == -404:
            user_info_1_item['mid'] = response_uid
            user_info_1_item['name'] = ''
            user_info_1_item['sex'] = ''
            user_info_1_item['face'] = ''
            user_info_1_item['sign'] = ''
            user_info_1_item['level'] = ''
        else:
            user_info_1 = user_info_1['data']
            # mid
            user_info_1_item['mid'] = user_info_1['mid']
            # 昵称
            user_info_1_item['name'] = user_info_1['name']
            # 性别
            user_info_1_item['sex'] = user_info_1['sex']
            # 头像
            user_info_1_item['face'] = user_info_1['face']
            # 个性签名
            user_info_1_item['sign'] = user_info_1['sign']
            # 等级
            user_info_1_item['level'] = user_info_1['level']
            # headers
            user_info_1_item['headers'] = headers

            user_info_2_item = Userinfo_2Item()
            # mid
            user_info_2_item['mid'] = user_info_1['mid']
            url_2 = 'https://api.bilibili.com/x/relation/stat?vmid=' + \
                response_uid + '&jsonp=jsonp'
            try:
                response_2 = requests.get(url=url_2, headers=headers)
                user_info_2 = json.loads(response_2.text)['data']
                # 关注数
                user_info_2_item['following'] = user_info_2['following']
                # 粉丝数
                user_info_2_item['follower'] = user_info_2['follower']
                yield user_info_2_item
            except:
                logger.error(url_2)

            user_info_3_item = Userinfo_3Item()
            # mid
            user_info_3_item['mid'] = user_info_1['mid']
            url_3 = 'https://api.bilibili.com/x/space/upstat?mid=' + \
                response_uid + '&jsonp=jsonp'
            try:
                response_3 = requests.get(url=url_3, headers=headers)
                user_info_3 = json.loads(response_3.text)['data']
                # 播放数
                user_info_3_item['archive_view'] = user_info_3['archive']['view']
                # 阅读数
                user_info_3_item['article_view'] = user_info_3['article']['view']
                # 点赞数
                user_info_3_item['likes'] = user_info_3['likes']
                yield user_info_3_item
            except:
                logger.error(url_3)

        yield user_info_1_item
