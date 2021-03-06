import requests
from bs4 import BeautifulSoup
from datetime import  timedelta
import pandas as pd

def soup_url(url):
    try: 
        rss_feed = url
        response = requests.get(rss_feed)
        soup = BeautifulSoup(response.content, features="xml")
        soup.prettify()
    except Exception as e:
        print("scraping failed")
        print(e)
    return soup
        
def podcast_rssFeed_csv(url):
#  each item tag contains - title, link, pubDate, guid, description, post-id, itunes:duration, itunes:author,
#itunes:subtitle, itunes:episode, itunes:episodeType, itunes:summary, content:encoded
    try: 
        soup = soup_url(url)
        items = soup.findAll('item')
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
        try:    
            title = soup.find('title').text
            return df.to_csv('%s.csv'%(title), index = False, encoding= 'utf-8')
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

def bing_watch_potential(rss_url):
    try:
        soup = soup_url(rss_url)
        durations = soup.findAll('itunes:duration')
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

bing_watch_potential("https://servusgruezihallo.podigee.io/feed/mp3")
podcast_rssFeed_csv("https://servusgruezihallo.podigee.io/feed/mp3")
