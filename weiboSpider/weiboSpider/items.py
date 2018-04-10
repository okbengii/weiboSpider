# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    profile_url = scrapy.Field()
    statuses_count = scrapy.Field()
    verified = scrapy.Field()
    verified_type = scrapy.Field()
    close_blue_v = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    mbtype = scrapy.Field()
    urank = scrapy.Field()
    mbrank = scrapy.Field()
    follow_me = scrapy.Field()
    following = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()
    cover_image_phone = scrapy.Field()
    avatar_hd = scrapy.Field()
    like = scrapy.Field()
    like_me = scrapy.Field()

class WeiboBlogItem(scrapy.Item):
    user_id = scrapy.Field()
    screen_name = scrapy.Field()
    itemid = scrapy.Field()
    scheme = scrapy.Field()
    created_at = scrapy.Field()
    text = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    origin_url = scrapy.Field()