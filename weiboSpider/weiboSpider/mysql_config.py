# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from sqlalchemy import Column,String,create_engine, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT


engine = create_engine('mysql+mysqldb://root:1234@47.93.42.140:3306/weibodata?charset=utf8')
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()

class userinfo(Base):
	__tablename__ = 'userinfo'
	id = Column(Integer,primary_key = True,autoincrement=True)
	user_id = Column(String(255))
	screen_name = Column(String(255))
	profile_image_url = Column(String(255))
	profile_url = Column(String(255))
	statuses_count = Column(String(255))
	verified = Column(String(255))
	verified_type = Column(String(255))
	close_blue_v = Column(String(255))
	description = Column(LONGTEXT)
	gender = Column(String(255))
	mbtype = Column(String(255))
	urank = Column(String(255))
	mbrank = Column(String(255))
	follow_me = Column(String(255))
	following = Column(String(255))
	followers_count = Column(String(255))
	follow_count = Column(String(255))
	cover_image_phone = Column(String(255))
	avatar_hd = Column(String(255))
	like = Column(String(255))
	like_me = Column(String(255))

class userdata(Base):
	__tablename__ = 'userdata'
	id = Column(Integer,primary_key = True,autoincrement=True)
	user_id = Column(String(255))
	screen_name = Column(String(255))
	itemid = Column(String(255))
	scheme = Column(String(255))
	created_at = Column(DateTime)
	text = Column(LONGTEXT)
	reposts_count = Column(String(255))
	comments_count = Column(String(255))
	attitudes_count = Column(String(255))

def insert_user_info(user_data):
	flag = session.query(userinfo).filter(userinfo.user_id==user_data.user_id).all()
	if flag:
		print '已存在'
	else:
		session.add(user_data)
		session.commit()

def insert_user_data(user_data):
	flag = session.query(userdata).filter(userdata.itemid==user_data.itemid).all()
	if flag:
		print '已存在'
	else:
		session.add(user_data)
		session.commit()

def query_user_id():
	result = session.query(userinfo).all()
	user_list = []
	for item in result:
		user_list.append(item.user_id)
	return user_list
