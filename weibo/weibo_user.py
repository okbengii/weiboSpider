# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import random
import re
from Queue import Queue
from mysql_config import insert_user_info
from mysql_config import Userinfo
import re
import threading
from time import ctime,sleep
# 关注列表
url_follows = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_1266321801&luicode=10000011&lfid=1005051266321801&featurecode=20000320&type=uid&value=1266321801"
# 推荐列表
url_follows_recomm = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followersrecomm_-_1266321801&luicode=10000011&lfid=1005051266321801&featurecode=20000320&type=uid&value=1266321801&since_id=1497184436%7C20_1"
# 粉丝列表
url_fans = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_1266321801&luicode=10000011&lfid=1005051266321801&featurecode=20000320&type=uid&value=1266321801"


try:
	# python UCS-4 build的处理方式
	highpoints = re.compile(u'[\U00010000-\U0010ffff]')
except re.error:
# python UCS-2 build的处理方式
	highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

queue = Queue()

queue_page = Queue()
"""
获取 关注列表
"""
def get_followers(param,pageIndex):
	result = "https://m.weibo.cn/api/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=%s" % (param,pageIndex)
	return result
"""
获取 个人用户信息列表
"""
def get_user_info(param):
	result = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=100505%s" % (param,param)
	return result

headers = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

def crawl_user(url=None,uid=None,page=None):
	print "START CRAWL USER FOLLOWERS:" , url
	response = requests.request("GET", url, headers=headers)

	# 解析返回内容
	parse_followers(response.content,uid,page)

def crawl_user_info(url):
	print "START CRAWL USER INFO:" , url
	response = requests.request("GET", url, headers=headers)
	parse_user_info(response.content)

def parse_user_info(content):
	if "data" in content:
		json_data = json.loads(content)['data']
		user_info = json_data["userInfo"]

		user_id = user_info['id']
		screen_name = user_info['screen_name']
		profile_image_url = user_info['profile_image_url']
		profile_url = user_info['profile_url']
		statuses_count = user_info['statuses_count']
		verified = user_info['verified']
		verified_type = user_info['verified_type']
		close_blue_v = user_info['close_blue_v']
		description = highpoints.sub(u'??', user_info['description'])
		gender = user_info['gender']
		mbtype = user_info['mbtype']
		urank = user_info['urank']
		mbrank = user_info['mbrank']
		follow_me = user_info['follow_me']
		following = user_info['following']
		followers_count = user_info['followers_count']
		follow_count = user_info['follow_count']
		cover_image_phone = user_info['cover_image_phone']
		avatar_hd = user_info['avatar_hd']
		like = user_info['like']
		like_me = user_info['like_me']
		item = Userinfo(user_id=user_id,screen_name=screen_name,profile_image_url=profile_image_url,
						profile_url=profile_url, statuses_count=statuses_count, verified=verified,
						verified_type=verified_type, close_blue_v=close_blue_v, description=description,
						gender=gender, mbtype=mbtype, urank=urank,
						mbrank=mbrank, follow_me=follow_me, following=following,
						followers_count=followers_count, follow_count=follow_count, cover_image_phone=cover_image_phone,
						avatar_hd=avatar_hd, like=like, like_me=like_me)
		insert_user_info(item)


def parse_followers(content,uid,page):
	if "data" in content:
		json_data = json.loads(content)['data']
		if 'cards' in json_data:
			follower_data = json_data['cards']
			for item in follower_data:
				user_id = item['user']['id']
				queue.put(user_id)

		if 'cardlistInfo' in json_data:
			next_page = int(json_data['cardlistInfo']['page'])
			# 翻页
			if "maxPage" in json_data:
				maxPage = json_data['maxPage']
				if next_page <= int(maxPage):

					url = get_followers(uid,next_page)
					queue_page.put(url)
					# crawl_user(url,uid,next_page)

def crawl_user_info_spider():
	while not queue.empty():
		user_id = queue.get()
		user_info_url = get_user_info(user_id)
		crawl_user_info(user_info_url)

		url = get_followers(user_id, 1)
		queue_page.put(url)
		sleep(3)


def crawl_user_follower_spider():
	regex = re.compile("100505(.*?)_-_.*?WERS&page=(.*?)")
	while not queue_page.empty():

		url = queue_page.get()
		uid = re.findall(regex, url)[0][0]
		page = url[url.find("page=")+5:]
		crawl_user(url, uid, page)
		sleep(3)


def main():
	url = get_followers(3870736479,1)
	crawl_user(url,3870736479,1)

	try:
		t1 = threading.Thread(target=crawl_user_follower_spider)
		t2 = threading.Thread(target=crawl_user_info_spider)
		t1.start()
		t2.start()
	except:
		print "Error: unable to start thread"

if __name__ == '__main__':
	main()