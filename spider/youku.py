# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
import bs4
import random
from spider.spider import Spider
from weibo.weibo_message import WeiboMessage
import re

HOME_URL = "https://so.youku.com/search_video/q_"


class YoukuParser(Spider):

    starName = ["张曼玉", "刘青云", "谢霆锋", "郑伊健", "谭咏麟", "古天乐", "黎明", "金城武", "陈冠希",
                "刘德华", "吴孟达", "郭富城", "王祖贤", "张敏", "张国荣", "陈百强", "梁朝伟", "李连杰",
                "曾志伟", "黄子华", "黄秋生", "杜汶泽", "温兆伦", "黄日华", "甄子丹", "张耀扬", "马浚伟",
                "冯倅帆", "洪金宝", "周星驰", "谭耀文", "黎耀祥", "郭晋安", "何嘉欣", "姜皓文", "郑晓峰",
                "谢天华", "钱嘉乐", "吴廷烨", "陈冠希", "元彪", "元华", "余文乐", "吴彦祖", "王晶",
                "张卫健", "任达华", "耿龙", "任达华", "梁家辉", "张曼玉", "宣萱", "蔡卓妍", "钟欣桐",
                "张柏芝", "钟嘉欣", "汪明荃", "郑秀文", "陈慧琳", "杨千嬅", "陈慧珊", "佘诗曼", "袁咏仪",
                "薛凯琪", "容祖儿", "唐宁", "钟丽缇", "刘嘉玲", "钟楚红", "叶子楣", "江若琳", "邓萃雯",
                "胡杏儿", "廖碧儿", "杨怡", "陈敏之", "李诗韵", "徐子珊", "叶翠翠", "陈法拉", "薛家燕",
                "米雪", "赵雅芝", "梅艳芳", "关之琳", "杨恭如", "周丽淇", "应采儿", "张可颐", "王菲",
                "吴君如", "李嘉欣", "伍咏薇", "蔡少芬", "邱淑贞", "蒙嘉慧", "邵美琪", "黎姿", "朱茵",
                "翁虹", "莫文蔚", "李彩桦", "傅颖", "官恩娜", "王若琳", "乐基儿", "梁洛施", "邓丽欣",
                "陈慧娴", "万琦文", "叶璇", "张文慈", "胡定欣", "郭可盈", "文颂娴", "李若彤", "杨思琦",
                "翁美玲", "李诗韵", "周慧敏", "陈松伶"]
    def __init__(self):
        super(YoukuParser, self).__init__(HOME_URL)

    #这里是获取一条代发的微博信息
    def get_weibo_message(self):
        #随机查询明星
        star_count = len(self.starName)
        qname = self.starName[random.randint(0, star_count -1)]
        self.home_url = self.home_url + qname;

        #获取页面信息
        json_text = self.download_text()
        items = self.getItems(json_text)

        msg = ''
        count = len(items)
        if count > 0:
            index = random.randint(0, count - 1)
            msg = items[index]

        return WeiboMessage(msg)

    def getItems(self, jsonStr):
        items = []

        html = self.download_text()
        soup = bs4.BeautifulSoup(html, "html.parser")
        # < h2
        # class ="spc-lv-1" >
        #
        # < a
        # target = "_blank"
        # data - spm = "dtitle"
        # title = "向华强寿宴周星驰没来, 成龙也没来? 向太回应: 我从没让成龙下跪"
        # href = "//v.youku.com/v_show/id_XMzk3NDM4MzY2MA==.html" > 向华强寿宴 < em
        #
        # class ="hl" > 周 < / em > < em class ="hl" > 星驰 < / em > 没来, 成龙也没来? 向太回应: 我从没让成龙下跪 <
        #
        # / a >

        # bpmodule-main > div.sk-result-list  {'type': 'text/javascript'}  bigview.view(


        divs = soup.findAll(attrs={'type': 'text/javascript'})
        for div in divs:
            if div.contents[0].find("bigview.view(") > -1:
                innertext = re.findall(r'\((.*)\)', div.contents[0])
                nodes = json.loads(innertext[0])
                htmltext = nodes["html"]
                if htmltext:
                    soup2 = bs4.BeautifulSoup(htmltext, "html.parser")
                    nodes = soup2.find_all("h2", class_="spc-lv-1")
                    msg = ''
                    for node in nodes:
                        a = node.a
                        if a:
                            str = a.text
                            if str and len(str) > 20:
                                title = str.strip()
                                url = a.get('href')
                                url = "https:"+url
                                item = "%s %s" % (title, url)
                                items.append(item)
                    break

        return items

