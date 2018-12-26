# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
import random
from spider.spider import Spider
from weibo.weibo_message import WeiboMessage

HOME_URL = "http://api.vc.bilibili.com/board/v1/ranking/top?page_size=20&next_offset=&tag=%E4%BB%8A%E6%97%A5%E7%83%AD%E9%97%A8&platform=pc"


class BilibiliParser(Spider):

    def __init__(self):
        super(BilibiliParser, self).__init__(HOME_URL)

    #这里是获取一条代发的微博信息
    def get_weibo_message(self):
        json_text = self.download_text()
        items = self.getItems(json_text)
        msg = ''
        count = len(items)
        if count > 0:
            index = random.randint(0, count - 1)
            msg = items[index]
            # for item in items:
            #     msg = WeiboMessage(item)
            #     if msg.text.find("电影") > -1 or msg.text.find("周瑞发") > -1 or msg.text.find("周星驰") > -1 \
            #             or msg.text.find("张曼玉") > -1 or msg.text.find("刘德华") > -1 or msg.text.find("吴孟达") > -1 \
            #             or msg.text.find("郭富城") > -1 or msg.text.find("王祖贤") > -1 or msg.text.find("张敏") > -1 \
            #             or msg.text.find("张国荣") > -1 or msg.text.find("陈百强") > -1 or msg.text.find("梁朝伟") > -1 \
            #             or msg.text.find("李连杰") > -1 or msg.text.find("张卫健") > -1 or msg.text.find("任达华") > -1:
            #         return msg;

        return WeiboMessage(msg)

    def getItems(self, jsonStr):
        items = []

        nodes = json.loads(jsonStr)
        results = nodes['data']['items']
        for node in results:
            url = node['item']['share_url']   # 小视频的下载链接  video_playurl  share_url
            msg = node['item']['description']     # 小视频的标题
            item = "%s %s" % (msg, url)
            items.append(item)
        return items
