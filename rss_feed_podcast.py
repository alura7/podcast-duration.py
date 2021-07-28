import requests
from bs4 import BeautifulSoup
import time
import sys
from datetime import  timedelta
import pandas as pd
from urllib.parse import urlparse

url = "https://www.geschichte.fm/feed/mp3/"

url2 = 'http://abc.hostname.com/somethings/anything/'
def url_parse(url):
    try:
        t = urlparse(url).netloc
        print ('.'.join(t.split('.')[1:]))
        name = '.'.join(t.split('.')[1:])
        
    except Exception as e:
        print(e)
        name = "none"
    return name

def podcast_rssFeed_csv(url):
    try: 
        rss_feed = url
        response = requests.get(rss_feed)
        scrape = BeautifulSoup(response.content, features="xml")
        scrape.prettify()
    except Exception as e:
        print("scraping failed")
        print(e)
#  each item tag contains - title, link, pubDate, guid, description, post-id, itunes:duration, itunes:author,
#itunes:subtitle, itunes:episode, itunes:episodeType, itunes:summary, content:encoded
    try: 
        items = scrape.findAll('item')
        new_itemsList = []
        for item in items:
            items_list = {}
            items_list['title'] = item.title.text
            items_list['link'] = item.link.text
            items_list['description'] = item.description.text
            items_list['pubDate'] = item.pubDate.text
            items_list['duration'] = [duration.text for duration in item.findAll('itunes:duration')][0]
            items_list['author'] = [author.text for author in item.findAll('itunes:author')][0]
            new_itemsList.append(items_list)

        df = pd.DataFrame(new_itemsList, columns = ['title','link','description','pubDate','duration','author'])
        csv_name = url_parse(url) 
        return df.to_csv('%s.csv'%(csv_name), index = False, encoding= 'utf-8')
    except Exception as e:
        print(e)

def how_long(rss_url):
    try: 
        response = requests.get(rss_url)
        scrape = BeautifulSoup(response.content, features="xml")
        scrape.prettify()
    except Exception as e:
        print(e)
    try:
        durations = scrape.findAll('itunes:duration')
        durations_list =[]
        for duration in durations:
            durations_list.append(duration.text)
        totalSecs = 0
        if ':' in durations_list[0]:
            for tm in durations_list:
                timeParts = [int(s) for s in tm.split(':')]
                totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
            totalSecs, sec = divmod(totalSecs, 60)
            hr, min = divmod(totalSecs, 60)
            day, hr = divmod(hr, 24)
            print ("%d days and %d hours and %02d minutes and %02d seconds" % (day, hr, min, sec))
        else:
            try:
                for tm in durations_list:
                    parts = str(timedelta(seconds=int(tm)))
                    timeParts = [int(s) for s in parts.split(':')]
                    totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
                totalSecs, sec = divmod(totalSecs, 60)
                hr, min = divmod(totalSecs, 60)
                day, hr = divmod(hr, 24)
                print ("%d days and %d hours and %02d minutes and %02d seconds" % (day, hr, min, sec))
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    

how_long("https://servusgruezihallo.podigee.io/feed/mp3")
podcast_rssFeed_csv("https://servusgruezihallo.podigee.io/feed/mp3")