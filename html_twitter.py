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

def image_download(url, output):
    opener = urllib2.build_opener()
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    img_file = open(output, 'wb')
    img_file.write(opener.open(req).read())
    img_file.close()

tree = lxml.html.parse("twitter.html")
html = tree.getroot()
rink = html.xpath('//*[@id="stream-items-id"]/span/img')

tw_url = "https://pbs.twimg.com/media/"
conn = sqlite3.connect('twitter.db')
c = conn.cursor()
count = 1
for a in rink:
    img_name = a.get("src").split("/")[-1] #画像ファイル名
    img_url = tw_url + img_name #画像のurl

    query = 'SELECT * FROM twitter WHERE url = "' + img_url + '"'
    c.execute(query)
    if c.fetchone() is not None:
        print("skip")
        continue

    print count
    count += 1
    output = "twitter/" + img_name
    image_download(img_url, output)
    c.execute('INSERT INTO twitter(name, url) VALUES(?,?)', (img_name, img_url))
    conn.commit()

c.close()