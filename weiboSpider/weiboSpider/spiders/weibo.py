# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from weiboSpider.items import WeibospiderItem
import scrapy
import json
import re
import logging

headers = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
def get_user_info(param):
	result = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=100505%s" % (param,param)
	return result

def get_followers(param,pageIndex):
	result = "https://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=%s" % (param,pageIndex)
	return result

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    # allowed_domains = ['weibo']
    # start_urls = ['http://weibo/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'weiboSpider.pipelines.WeibospiderPipeline': 300
        }
    }

    def start_requests(self):
    	first_url = "https://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=%s" % (2286908003,1)
    	yield scrapy.Request(first_url,callback=self.parse,headers=headers,dont_filter=True,meta={"uid":2286908003})

    def parse(self, response):
        logging.info("CRAWL URL:" + response.url)
        uid = response.meta['uid']
        if 'data' in response.body:
            json_data = json.loads(response.body)['data']
            if "cards" in json_data:
                follower_data = json_data['cards']
                for item in follower_data:
                    user_id = item['user']['id']
                    # 关注者的 个人信息
                    follower_user_url = get_user_info(user_id)
                    yield scrapy.Request(follower_user_url,callback=self.parse_user_content,headers=headers,dont_filter=True,priority=1)

                    # 关注者的关注者
                    follower_url = get_followers(user_id,1)
                    yield scrapy.Request(follower_url, callback=self.parse, headers=headers,
                                         dont_filter=True,meta={"uid":user_id},priority=0)
        if 'cardlistInfo' in json_data:
            next_page = int(json_data['cardlistInfo']['page'])
            # 翻页
            if "maxPage" in json_data:
                maxPage = json_data['maxPage']
                if next_page <= int(maxPage):
                    follower_url = get_followers(uid, next_page)
                    yield scrapy.Request(follower_url, callback=self.parse, headers=headers,
                                         dont_filter=True,meta={"uid":uid},priority=1)

    def parse_user_content(self,response):
        logging.info("CRAWL URL:" + response.url)
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        if "data" in response.body:
            json_data = json.loads(response.body)['data']

            item =  WeibospiderItem()

            user_info = json_data["userInfo"]

            item["user_id"] = user_info['id']
            item["screen_name"] = user_info['screen_name']
            item["profile_image_url"] = user_info['profile_image_url']
            item["profile_url"] = user_info['profile_url']
            item["statuses_count"] = user_info['statuses_count']
            item["verified"] = user_info['verified']
            item["verified_type"] = user_info['verified_type']
            item["close_blue_v"] = user_info['close_blue_v']
            item["description"] = highpoints.sub(u'??', user_info['description'])
            item["gender"] = user_info['gender']
            item["mbtype"] = user_info['mbtype']
            item["urank"] = user_info['urank']
            item["mbrank"] = user_info['mbrank']
            item["follow_me"] = user_info['follow_me']
            item["following"] = user_info['following']
            item["followers_count"] = user_info['followers_count']
            item["follow_count"] = user_info['follow_count']
            item["cover_image_phone"] = user_info['cover_image_phone']
            item["avatar_hd"] = user_info['avatar_hd']
            item["like"] = user_info['like']
            item["like_me"] = user_info['like_me']
            yield item
