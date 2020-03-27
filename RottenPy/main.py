from newspaper import Article
from bs4 import BeautifulSoup
from RottenPy import Movie
from RottenPy import Critiq

import json


class API:
    def __init__(self):
        pass

    def _parse(self, url):
        """

        :param url:
        :return: json file containing the matadata
        """
        art = Article(url)
        art.download()
        art.parse()
        soup = BeautifulSoup(art.html)
        found = soup.find('script')
        txt = soup.find('script').text
        jsn = json.loads(soup.find('script').text.strip())
        return json.loads(soup.find('script').text.strip())

    def _get_url(self, _id, url_type):
        if "https://rottentomatoes" in _id:
            return _id
        movie_base_string = 'https://www.rottentomatoes.com/m/'
        critic_base_string = 'https://www.rottentomatoes.com/critic/'
        if url_type == 'm':
            return movie_base_string + _id
        elif url_type == 'c':
            return critic_base_string + _id + '/movies'
        else:
            return None

    def get_critic_info(self, critic_id):
        data = self._parse(critic_id)
        data = data['@graph']
        person = data[0]
        movies = data[1]

        name = person['name']
        affiliates = []
        for item in person['worksFor']:
            affiliates.append(item['name'])

        reviews = []
        for movie in movies['itemListElement']:
            reviews.append({
                'review_heading': movie['item']['description'],
                'review_body': movie['item']['reviewBody'],
                'review_url': movie['item']['url'],
                'movie_name': movie['item']['itemReviewed']['name'],
                'movie_url': movie['item']['itemReviewed']['sameAs'],
                'review_rating': movie['item']['reviewRating']['ratingValue'],
                'review_tomatometer': movie['item']['reviewRating']['tomatometer']
            })
        return Critiq.Critiq(name, affiliates, reviews)

    def get_movie_info(self, movie_id):
        data = self._parse(self._get_url(movie_id, 'm'))
        title = data['name']
        rating = data['contentRating']
        url = data['url']
        productionhouses = data['productionCompany']
        tomatometer = data['aggregateRating']['ratingValue']
        tomatometer_count = data['aggregateRating']['reviewCount']
        reviews = []
        for review in data['review']:
            review_dict = {}
            try:
                review_dict['author_name'] = review['author']['name']
                review_dict['rating'] = review['reviewRating']
                review_dict['review_text'] = review['reviewBody']
                review_dict['critic_url'] = review['author']['url']
            except Exception as E:
                continue
            reviews.append(review_dict)
        cast = []
        for actor in data['actors']:
            temp_dict = dict()
            temp_dict['name'] = actor['name']
            temp_dict['url'] = actor['sameAs']
            cast.append(temp_dict)

        characters = data['character']
        genre = data['genre']

        return Movie.Movie(title, url, productionhouses, rating, tomatometer_count, reviews, cast, characters, genre)

    def get_top_streaming(self):
        art = Article('https://www.rottentomatoes.com')
        art.download()
        art.parse()
        soup = BeautifulSoup(art.html)
        temp = soup.find('table', {'class': 'media-lists__table'})
        to_return = []
        for item in temp.find_all('tr'):
            tds = item.find_all('td')
            to_return.append({
                'movie_title': tds[1].a.contents[0],
                'movie_url': 'https://rottentomatoes.com' + str(tds[1].a['href']),
                'movie_rating': tds[0].find_all('span')[1].contents[0]
            })
        return to_return

    def get_tv_tonight(self):
        art = Article('https://www.rottentomatoes.com')
        art.download()
        art.parse()
        soup = BeautifulSoup(art.html)
        temp = soup.find('section', {'id': 'new-tv-tonight'}).find('table')
        to_return = []
        for item in temp.find_all('tr'):
            tds = item.find_all('td')
            to_return.append({
                'movie_title': tds[1].a.contents[0].strip(),
                'movie_url': 'https://rottentomatoes.com' + str(tds[1].a['href']),
                'movie_rating': tds[0].find_all('span')[1].contents[0]
            })
        return to_return

    def get_top_classics(self):
        art = Article('https://www.rottentomatoes.com')
        art.download()
        art.parse()
        soup = BeautifulSoup(art.html)
        temp = soup.find('section', {'id': 'dynamic-list'}).find('table')
        to_return = []
        for item in temp.find_all('tr'):
            tds = item.find_all('td')
            to_return.append({
                'movie_title': tds[1].a.contents[0].strip(),
                'movie_url': 'https://rottentomatoes.com' + str(tds[1].a['href']),
                'movie_rating': tds[0].find_all('span')[1].contents[0]
            })
        return to_return

    def get_top_tv(self):
        art = Article('https://www.rottentomatoes.com')
        art.download()
        art.parse()
        soup = BeautifulSoup(art.html)
        temp = soup.find('section', {'id': 'popular-tv'}).find('table')
        to_return = []
        for item in temp.find_all('tr'):
            tds = item.find_all('td')
            to_return.append({
                'movie_title': tds[1].a.contents[0].strip(),
                'movie_url': 'https://rottentomatoes.com' + str(tds[1].a['href']),
                'movie_rating': tds[0].find_all('span')[1].contents[0]
            })
        return to_return

    def get_top_100_movies(self):
        art = Article('https://www.rottentomatoes.com/top/bestofrt/')
        art.download()
        art.parse()
        soup = BeautifulSoup(art.html)
        temp = soup.find('table', {'class': 'table'})
        to_return = []
        for item in temp.find_all('tr'):
            tds = item.find_all('td')
            if len(tds) > 1:
                to_return.append({
                    'movie_title': tds[2].a.contents[0].strip(),
                    'movie_url': 'https://rottentomatoes.com' + str(tds[2].a['href']),
                    'movie_rating': str(tds[1].find_all('span', {'class': 'tMeterScore'})[0].text)
                })
        return to_return