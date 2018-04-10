# 微博数据抓取

环境：

scrapy

mysql5.7

scrapyd

# 抓取用户爬虫

	weibo
	
	调用 api:

		curl http://47.93.42.140:6800/schedule.json -d project=weiboSpider -d spider=weibo
	
	查看 爬虫节点：
		curl http://47.93.42.140:6800/listspiders.json?project=weiboSpider
		
	终止爬虫：
		curl http://47.93.42.140:6800/cancel.json -d project=weiboSpider -d job=82f5e8f23c9e11e8b5de00163e0cb35d

# 抓取用户微博爬虫
	
	weiboBlog
	
	调用 api:

		curl http://47.93.42.140:6800/schedule.json -d project=weiboSpider -d spider=weiboBlog