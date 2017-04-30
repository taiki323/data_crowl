import urllib2
from requests_oauthlib import OAuth1Session
import json
import requests
from datetime import datetime
import urllib,urllib2
import lxml.html
from PIL import Image
import time, sqlite3
import threading

folder = 'twitter/'

def monthtonum(month):
    if month == "Apr":
        return str(04)
    if month == "Mar":
        return str(03)

def date_format(created_at):
    list = created_at.split(" ")
    year = str(list[-1])
    month = monthtonum(str(list[1]))
    date = str(list[2])
    time = str(list[3])
    datetime = year + "-" + month + "-" + date + "_" + time + "_JST"

    return datetime

def image_download(url, output):
	opener = urllib2.build_opener()
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	img_file = open(output, 'wb')
	img_file.write(opener.open(req).read())
	img_file.close()

oath_key_dict = {
    "consumer_key": "",
    "consumer_secret": "",
    "access_token": "",
    "access_token_secret": ""
}
def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

def tweet_search(search_word, oath_key_dict, datetime):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": unicode(search_word),
        #"lang": "ja",
        "result_type": "recent",
        "count": "2000",
        "until": datetime
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    tweets = json.loads(responce.text)
    return tweets

count = 420
datetime = "2017-4-30_00:00:00_JST"
for i in range(40):
    tweets = tweet_search("#paintschainer", oath_key_dict, datetime)
    if(len(tweets["statuses"]) == 0):
        time.sleep(16)
        continue
    for tweet in tweets["statuses"]:
        try:
            img_url = tweet.get(u'extended_entities').get(u'media')
        except:
            continue
        for url in img_url:
            filename = folder + "PaintsChainer" + str(count) + ".jpg"
            image_download(url[u'media_url'],filename)

            conn = sqlite3.connect('twitter.db')
            c = conn.cursor()
            query = 'SELECT * FROM twitter WHERE url = "' + url[u'media_url'] + '"'
            c.execute(query)
            if c.fetchone() is not None:
                print("skip")
                continue
            query = 'INSERT INTO twitter(url) VALUES("' + url[u'media_url'] +'")'
            c.execute(query)
            conn.commit()
            conn.close()
            print url[u'media_url']
        print(count)
        count += 1

    created_at = tweet[u'created_at']
    datetime = date_format(created_at)
    print datetime

print "end"