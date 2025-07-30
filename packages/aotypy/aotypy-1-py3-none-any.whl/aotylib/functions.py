import requests
import cloudscraper
from bs4 import BeautifulSoup
import time
def get_soup(url):
        scraper = cloudscraper.create_scraper()
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.albumoftheyear.org/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        }
        session = requests.Session()
        session.headers.update(headers)
        response = scraper.get(url) 
        return BeautifulSoup(response.text, "html.parser")

def album_info(link):
        soup = get_soup(link)
        try:
            genres = [(x.text, f'albumoftheyear.org{x.get('href')}') for x in soup.find_all('div', class_ = 'detailRow')[3].find_all('a')]
        except:
            genres = []
        name = soup.find('h1', class_= 'albumTitle').text
        artist = soup.find('div', class_ = 'artist').text
        critic_score = soup.find('div', class_= 'albumCriticScoreBox').find('a').text
        user_score = soup.find('div', class_='albumUserScoreBox').find('a').text
        release_date = soup.find_all('div', class_ = 'detailRow')[0].text
        format = soup.find_all('div', class_ = 'detailRow')[1].text
        try:
            labels = [(x.text, f'albumoftheyear.org{x.get('href')}') for x in soup.find_all('div', class_ = 'detailRow')[2].find_all('a')]
        except:
            labels = []
        try:
            producers = [(x.text, f'albumoftheyear.org{x.get('href')}') for x in soup.find_all('div', class_ = 'detailRow')[4].find_all('a')]
        except:
            producers = []
        try:
            writers = [(x.text, f'albumoftheyear.org{x.get('href')}') for x in soup.find_all('div', class_ = 'detailRow')[5].find_all('a')]
        except:
            writers = []
        try:
            tags = [(x.text, f'albumoftheyear.org{x.get('href')}') for x in soup.find_all('div', class_ = 'detailRow')[6].find_all('a')]
        except:
            tags = []
        time.sleep(1)
        return {'name' : name, 
                'artist': artist, 
                'critic_score' :critic_score, 
                'user_score': user_score, 
                'release_date': release_date, 
                'format': format, 
                'genres': genres, 
                'labels': labels, 
                'producers': producers,
                'writers': writers,
                'tags': tags}

def artist_info(link):
    soup = get_soup(link)
    name = soup.find('h1', class_ = 'artistHeadline').text
    albums = [(x.find_all('a')[1].text, f'albumoftheyear.org{x.find('a').get('href')}') for x in soup.find('div', id = 'albumOutput').find_all('div', class_= 'albumBlock small')]
    time.sleep(1)
    return {
         'name': name,
         'albums': albums
    }

def new_releases():
    soup = get_soup('https://www.albumoftheyear.org/')
    t = soup.find('span', id ='homeNewReleases')
    albums = [(x.find_all('a')[1].text, f'albumoftheyear.org{x.find('a').get('href')}') for x in t.find_all('div', class_= 'albumBlock')]
    time.sleep(1)
    return albums
