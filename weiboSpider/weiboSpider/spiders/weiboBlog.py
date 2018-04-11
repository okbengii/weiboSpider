# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from weiboSpider.items import WeiboBlogItem
from weiboSpider.mysql_config import userdata,query_user_id
import scrapy
import json
import re
import logging

def parse_time(time_str):
    now_time = time.strptime(time_str, "%Y-%m-%d")
    y, m, d, h, mm, s = now_time[0:6]
    update_time = datetime.date(y, m, d)
    return update_time

import datetime
import time
def get_url(uid,pageIndex):
    url = "https://m.weibo.cn/api/container/getIndex?uid=%s&featurecode=20000320&type=uid&value=%s&containerid=107603%s&page=%s" % (uid,uid,uid,pageIndex)
    return url

headers = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

class WeiboBlog(scrapy.Spider):
    name = "weiboBlog"

    custom_settings = {
        'ITEM_PIPELINES': {
            'weiboSpider.pipelines.WeiboBlogPipeline': 300
        }
    }
    def start_requests(self):
        user_list = query_user_id()
        for item in user_list:
            url = get_url(item, 1)
            yield scrapy.Request(url,callback=self.parse,headers=headers,dont_filter=True,meta={"uid":item,"pageIndex":1})

    def parse(self,response):
        logging.info("CRAWL URL:" + response.url)
        try:
            # python UCS-4 build的处理方式
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # python UCS-2 build的处理方式
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        json_data = json.loads(response.body)["data"]
        user_message = json_data['cards']

        uid = response.meta["uid"]
        pageIndex = response.meta["pageIndex"]
        flag = True # 判断是否需要翻页
        if len(user_message) != 0:
            for message in user_message:
                if "mblog" in message:
                    itemid = message['mblog']['idstr']
                    scheme = message['scheme']
                    created_at = message['mblog']['created_at']

                    pattern = "[0-9]*?-[0-9]*?-[0-9]*?"
                    if created_at.find(u"小时前") != -1:
                        created_at = datetime.date.today()
                    elif created_at.find(u"昨天") != -1:
                        now = datetime.date.today()
                        delta = datetime.timedelta(days=1)
                        created_at = now - delta
                    elif created_at.find(u"前天") != -1:
                        now = datetime.date.today()
                        delta = datetime.timedelta(days=2)
                        created_at = now - delta
                    elif re.match(pattern, created_at):
                        created_at = parse_time(created_at)
                    elif created_at.find(u"分钟前") != -1:
                        created_at = datetime.date.today()
                    elif created_at.find(u"刚刚") != -1:
                        created_at = datetime.date.today()
                    else:
                        created_at = parse_time(str(datetime.datetime.now().year) + "-" + created_at)
                    text = highpoints.sub(u'??',re_h.sub('',message['mblog']['text']))
                    reposts_count = message['mblog']['reposts_count']
                    comments_count = message['mblog']['comments_count']
                    attitudes_count = message['mblog']['attitudes_count']
                    user_id = message['mblog']['user']['id']
                    screen_name = highpoints.sub(u'??', message['mblog']['user']['screen_name'])
                    item = WeiboBlogItem()
                    item["itemid"] = itemid
                    item["scheme"] = scheme
                    item["created_at"] = created_at
                    item["text"] = text
                    item["reposts_count"] = reposts_count
                    item["comments_count"] = comments_count
                    item["attitudes_count"] = attitudes_count
                    item["user_id"] = user_id
                    item["screen_name"] = screen_name
                    item["origin_url"] = response.url

                    now_time = datetime.date.today()
                    thrDay = now_time + datetime.timedelta(days=-3)
                    if thrDay > created_at:
                        flag = False
                        break
                    yield item
        if "msg" not in json.loads(response.body):
            if flag:
                url = get_url(uid, pageIndex + 1)
                yield scrapy.Request(url, callback=self.parse, headers=headers, dont_filter=True,
                                     meta={"uid": uid, "pageIndex": pageIndex + 1})