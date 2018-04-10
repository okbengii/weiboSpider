# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import random
import re
from Queue import Queue
from mysql_config import insert_user_info,query_user_id,insert_user_data
from mysql_config import Userinfo,Userdata
import re
import threading
from time import ctime,sleep
import datetime
import time
import sys
sys.setrecursionlimit(1000000)

try:
	# python UCS-4 build的处理方式
	highpoints = re.compile(u'[\U00010000-\U0010ffff]')
except re.error:
# python UCS-2 build的处理方式
	highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

headers = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

def parse_time(time_str):
        now_time = time.strptime(time_str, "%Y-%m-%d")
        y,m,d,h,mm,s = now_time[0:6]
        update_time = datetime.datetime(y,m,d,h,mm,s)
        return update_time

def get_url(uid,pageIndex):
	url = "https://m.weibo.cn/api/container/getIndex?uid=%s&featurecode=20000320&type=uid&value=%s&containerid=107603%s&page=%s" % (uid,uid,uid,pageIndex)
	return url
def crawler_user_message(url,uid,pageIndex):
    print "START CRAWL URL:",url
    response = requests.request("GET", url, headers=headers)
    parse_content(response.content,uid,pageIndex)

def parse_content(content,uid,pageIndex):

    json_data = json.loads(content)["data"]
    user_message = json_data['cards']
    if len(user_message) != 0:
        for message in user_message:
            if "mblog" in message:
                print message
                itemid = message['mblog']['idstr']
                scheme = message['scheme']
                created_at = message['mblog']['created_at']

                pattern = "[0-9]*?-[0-9]*?-[0-9]*?"
                if created_at.find(u"小时前") != -1:
                    created_at = datetime.datetime.now()
                elif created_at.find(u"昨天") != -1:
                    now = datetime.datetime.now()
                    delta = datetime.timedelta(days=1)
                    created_at = now - delta
                elif created_at.find(u"前天") != -1:
                    now = datetime.datetime.now()
                    delta = datetime.timedelta(days=2)
                    created_at = now - delta
                elif re.match(pattern, created_at):
                    created_at = parse_time(created_at)
                else:
                    created_at = parse_time(str(datetime.datetime.now().year) + "-" + created_at)

                text = message['mblog']['text']
                reposts_count = message['mblog']['reposts_count']
                comments_count = message['mblog']['comments_count']
                attitudes_count = message['mblog']['attitudes_count']
                user_id = message['mblog']['user']['id']
                screen_name = message['mblog']['user']['screen_name']
                item = Userdata(user_id=user_id, screen_name=screen_name, itemid=itemid,
                                scheme=scheme, created_at=created_at, text=text,
                                reposts_count=reposts_count, comments_count=comments_count,
                                attitudes_count=attitudes_count)
                insert_user_data(item)
            # next_page = json_data['cardlistInfo']['page']
            if "msg" not in json_data:
                url = get_url(uid, pageIndex + 1)
                crawler_user_message(url, uid, pageIndex + 1)

def main():
	user_list = query_user_id()
	for item in user_list:
		url = get_url(item,1)
		crawler_user_message(url,item,1)

if __name__ == '__main__':
	main()