# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import urllib,urllib2
import lxml.html
from PIL import Image
import time, sqlite3
import threading
import os
import re

global count
count = 1
lock = threading.Lock()

def img_resize(img):
	try:
		img_src = Image.open(img)
	except:
		return 0
	resizedImg = img_src.resize((500,500))
	resizedImg.save(img)

def image_download(url, output):
	opener = urllib2.build_opener()
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	img_file = open(output, 'wb')
	img_file.write(opener.open(req).read())
	img_file.close()
	#thread1 = threading.Thread(target=img_resize(output), name="thread1")
	#thread1.start()

def img_page(a):
	global count
	kakutyou = "jpg"
	taglist = []

	php = a[0].attrib['href']
	php = str(php)
	url2 = "http://safebooru.org/" + php #個別画像のリンク
	target_html = requests.get(url2).text
	html = lxml.html.fromstring(target_html)

	try:
		img = html.xpath('//*[@id="image"]')
		img = "http:" + img[0].get('src') #画像のurl
		tags = html.xpath('//*[@id="tag-sidebar"]/li/a') #tag
		for tag in tags:
			taglist.append(tag.text)
	except:
		return

	try:
		kakutyoushi = img.split(".")[-1].split("?")[0]
		if kakutyoushi == "png":
			kakutyou = kakutyoushi
		if kakutyoushi == "gif":
			return
	except:
		print "no question"

	#排他
	lock.acquire()
	tmp = count
	filename = str(tmp) + "." + kakutyou
	count += 1
	lock.release()

	print(str(tmp) + " url2=" + url2)
	print("img_url=" + img)
	image_download(img, "safebooru/" + filename)

	#排他
	lock.acquire()
	conn = sqlite3.connect('moe.db')
	c = conn.cursor()
	c.execute('INSERT INTO moe(name, tag) VALUES(?,?)', (filename, str(taglist)))
	conn.commit()
	conn.close()
	lock.release()

def safebooru():
	pid = 0
	i = 0
	for num in range(0,5000):
		url = "http://safebooru.org/index.php?page=post&s=list&tags=1girl&pid=" + str(pid)
		target_html = requests.get(url).text
		html = lxml.html.fromstring(target_html)
		rink = html.xpath("//span[*]")
		for a in rink:
			thread = "thread" + str(i)
			threading.Thread(target=img_page, name=thread,args=(a,)).start()
			#img_page(a)
			time.sleep(1)
			i += 1
		pid += 40


if __name__ == '__main__':
	safebooru()
