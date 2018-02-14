import urllib
from bs4 import BeautifulSoup

def search_url(title):
  return 'https://www.bbc.co.uk/iplayer/search?{}'.format(
      urllib.parse.urlencode({'q':title}))

def programme_id(title):
  urls = []
  with urllib.request.urlopen(search_url(title)) as search_page:
    search_soup = BeautifulSoup(search_page.read(), 'html.parser')
    prog_block = search_soup.find('li', {'class':'programme'})
    return prog_block['data-ip-id']

def episodes(prog_id):
  progs = []
  with urllib.request.urlopen(
      'https://www.bbc.co.uk/programmes/{}/episodes/player'.
        format(prog_id)) as episodes_page:
    episodes_soup = BeautifulSoup(episodes_page.read(), 'html.parser')
    brand = episodes_soup.find('div', 
        {'class':'br-masthead__title'})('a')[0].text
    for episode in episodes_soup('div',{'class':'programme'}):
      prog = { 
        'brand': brand,
        'pid': episode['data-pid'],
        'episode_title': episode.find('span',{'class':'programme__title'})\
            .find('span',{'property':'name'}).text,
      }
      prog['episode'] = int(prog['episode_title'].split(' ')[-1])
      series_title = episode.find('span',{'class':'programme__subtitle'})\
            .find('span',{'property':'name'}).text
      prog['series'] = int(series_title.split(' ')[-1])
      progs.append(prog)
    return sorted(progs, key=lambda p: '{:2}:{:2}'.format(p['series'],p['episode']))
