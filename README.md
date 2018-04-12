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

	查看爬虫任务:
		curl http://47.93.42.140:6800/listjobs.json?project=weiboSpider
		
# 抓取用户微博爬虫
	
	weiboBlog
	
	调用 api:

		curl http://47.93.42.140:6800/schedule.json -d project=weiboSpider -d spider=weiboBlog
		
		
# 定时任务调度执行爬虫 
	
	环境： docker
	
	使用 docker 定时执行 python 文件

1. 构建 docker 的 python 环境：

	Dockerfile：
		'''
		FROM python
		RUN pip install apscheduler
		RUN pip install requests
		'''
		
2. 开始构建：

	docker build -t weibospider .
	weibospider 是构建的 docker 镜像名称

3. 运行 docker：
	
	docker run -p 9090:9090 -v /usr/local/project/weiboData/JobScheduler.py:/weibodata/JobScheduler.py --name weibocrawler weibospider python /weibodata/JobScheduler.py
	
	-v 前边部分表示宿主机位置，后边部分表示docker容器位置
	--name weibocrawler 表示唯一的容器标识
	
	
常用命令：

docker ps

docker ps -a

docker run 镜像名称 # 创建容器并执行

docker start/restart/stop 容器名称/容器id

docker rmi 镜像id（删除镜像前要先删除所有的容器）

docker rm 容器id

docker inspect weibocrawler # 查看容器详细信息