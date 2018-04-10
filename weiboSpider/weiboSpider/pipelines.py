# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from mysql_config import insert_user_info,insert_user_data,userinfo,userdata
import datetime


class WeibospiderPipeline(object):
    def process_item(self, item, spider):
        userInfo = userinfo(user_id=item["user_id"],screen_name=item["screen_name"],profile_image_url=item["profile_image_url"],
						profile_url=item["profile_url"], statuses_count=item["statuses_count"], verified=item["verified"],
						verified_type=item["verified_type"], close_blue_v=item["close_blue_v"], description=item["description"],
						gender=item["gender"], mbtype=item["mbtype"], urank=item["urank"],
						mbrank=item["mbrank"], follow_me=item["follow_me"], following=item["following"],
						followers_count=item["followers_count"], follow_count=item["follow_count"], cover_image_phone=item["cover_image_phone"],
						avatar_hd=item["avatar_hd"], like=item["like"], like_me=item["like_me"])
        insert_user_info(userInfo)
        return item

class WeiboBlogPipeline(object):
	def process_item(self, item, spider):

		now = datetime.datetime.now()
		userData = userdata(user_id=item["user_id"],screen_name=item["screen_name"],itemid=item["itemid"],
							scheme=item["scheme"], created_at=item["created_at"], text=item["text"],
							reposts_count=item["reposts_count"], comments_count=item["comments_count"], attitudes_count=item["attitudes_count"],
							origin_url = item["origin_url"],insert_time=now
							)
		insert_user_data(userData)
		return item