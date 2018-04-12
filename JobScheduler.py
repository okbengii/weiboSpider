# coding:utf-8
import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging.handlers
import logging
import requests
import binascii as B
import hashlib
from datetime import timedelta
from pymongo import MongoClient
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 日志
LOG_FILE = 'WeiboDataScheduler.log'
logging.basicConfig()
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.INFO)


base_url = "http://xxx:xxx/"


def scheduler(dict_data):
	scheduler_url = base_url + "schedule.json"
	content  = requests.post(scheduler_url, data= dict_data)
	response = json.loads(content.content)
	jobid = response["jobid"]
	status = response["status"]
	if status == "ok":
		logging.info("JOB:"+ jobid + "START SUCCEFULLY...")


def main():

	dict_data = {
		"project":"weiboSpider",
		"spider":"weiboBlog"
	}

	scheduler(dict_data)

def scheduler_Job():
	scheduler = BlockingScheduler()
	scheduler.add_job(main, 'cron', day_of_week ='0-6', hour=10, minute=50)
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit) as e:
		logger.error(e)
	finally:
		scheduler.shutdown()

if __name__ == '__main__':
	main()
