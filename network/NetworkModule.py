import sys
import time
from bs4 import BeautifulSoup

from models.dataclasses.Person import Person
from models.dataclasses.Relation import Relation
from network.SeleniumSessionHandler import SeleniumSessionHandler


class RequestManager:
    _session = None

    @staticmethod
    def init_session():
        RequestManager._session = SeleniumSessionHandler.get_session()

    @staticmethod
    def request(url):
        if RequestManager._session is None:
            RequestManager.init_session()
        RequestManager._session.get(url)
        return RequestManager._session.page_source

    @staticmethod
    def get_current_session():
        if RequestManager._session is None:
            RequestManager.init_session()
        return RequestManager._session


class NetworkModule:
    _root_link = 'https://www.kinopoisk.ru'

    @staticmethod
    def _parse_person(driver, url):
        driver.get(url)
        html = driver.page_source
        person_id = url.split('/')[-1]
        if person_id == '':
            person_id = url.split('/')[-2]
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('h1', {'class': 'styles_primaryName__1bsl8'}).text
        try:
            pic_url = soup.find('div', {'class': 'styles_sidebar__383xd'}).find('img').get('src')
        except:
            pic_url = ''
        return Person(person_id=person_id, full_name=name, url=pic_url)

    @staticmethod
    def get_actors(name):
        time.sleep(3)
        session = RequestManager.get_current_session()
        html = SeleniumSessionHandler.get_search_response(session, name)
        soup = BeautifulSoup(html, 'html.parser')
        hrefs = soup.find_all('a', {'data-type': 'person'})
        urls = []
        for href in hrefs:
            link = href.get('data-url')
            urls.append(f'{NetworkModule._root_link}{link}')
        urls = [link for link in urls if len(link.split('/')) == 5]
        result = []
        for url in urls:
            result.append(NetworkModule._parse_person(session, url))
        return result

    @staticmethod
    def _get_only_actors_rows(rows):
        result = []
        first_time = False
        for row in rows:
            if list(row.children)[1].text == '1.':
                if not first_time:
                    first_time = True
                else:
                    return result
            result.append(row)
        return result

    @staticmethod
    def has_name_collision(name):
        actors = NetworkModule.get_actors(RequestManager.get_current_session(), name)
        return len(actors) > 1

    @staticmethod
    def get_actors_with_name(name):
        return NetworkModule.get_actors(RequestManager.get_current_session(), name)

    @staticmethod
    def _check_genres(url, genres):
        if genres is None:
            return True
        if len(genres) == 0:
            return True
        html = RequestManager.request(url)
        soup = BeautifulSoup(html, 'html.parser')
        actual_genres = [i.text for i in [a for a in soup.find_all('a') if a.get('href') is not None]
                         if (len(i.get('href').split('navigator')) == 2) & (len(i.get('href').split('country')) == 1) &
                         (len([int(s) for s in i.get('href').split('/') if s.isdigit()]) == 0)]
        for genre in genres:
            if genre.lower() in [s.lower() for s in actual_genres]:
                return True
        return False

    @staticmethod
    def _check_years(url, year_from, year_to):
        if (year_from is None) & (year_to is None):
            return True
        html = RequestManager.request(url)
        soup = BeautifulSoup(html, 'html.parser')
        year_tokens = [i.text for i in [a for a in soup.find_all('a') if a.get('href') is not None]
                       if (len(i.get('href').split('navigator')) == 2) &
                       (len([int(s) for s in i.get('href').split('/') if s.isdigit()]) == 1)]
        if len(year_tokens) > 0:
            year = int(year_tokens[0])
        else:
            year = None
        if year is None:
            return False
        if year_from is not None:
            if year_to is not None:
                return (int(year_from) <= year) & (int(year_to) >= year)
            return int(year_from) <= year
        return int(year_to) >= year

    @staticmethod
    def _filter_films(url, params):
        html = RequestManager.request(url)
        soup = BeautifulSoup(html, 'html.parser')
        first_time = False
        result = []
        for item in soup.find_all('div', {'class': 'item'}):
            if item.find('span', {'class': 'num'}).text == '1':
                if not first_time:
                    first_time = True
                else:
                    break
            for film in [f'{NetworkModule._root_link}{i}' for i in
                         [a.get('href') for a in item.find_all('a')
                          if (len(a.get('href').split('votes')) == 1) & (len(a.get('href').split('top')) == 1)]]:
                result.append(film)
        return [i for i in result if (NetworkModule._check_genres(i, params.genres)) &
                (NetworkModule._check_years(i, params.start_year, params.end_year))]

    @staticmethod
    def get_relations(params):
        return NetworkModule.get_part(sys.maxsize, params)

    @staticmethod
    def get_part(upper, params):
        if upper == 0:
            upper = sys.maxsize
        html = RequestManager.request(f'{NetworkModule._root_link}/name/{params.person.person_id}/relations/')
        soup = BeautifulSoup(html, 'html.parser')
        rows = [a.parent.parent for a in soup.find_all('a') if len(a.text.split('фильмов:')) == 2]
        if params.actors_only:
            rows = NetworkModule._get_only_actors_rows(rows)
        rows = [a for a in rows if (params.threshold <= int(a.text.split('фильмов: ')[1].split('.')[0])) &
                (upper > int(a.text.split('фильмов: ')[1].split('.')[0]))]
        result = []
        for row in rows:
            person_url = row.find('a').get('href')
            person = NetworkModule \
                ._parse_person(RequestManager.get_current_session(), f'{NetworkModule._root_link}{person_url}')
            count = int(row.text.split('фильмов: ')[1].split('.')[0])
            filtered_count = count
            if params.genres is not None:
                if len(params.genres) != 0:
                    list_url = row.find('a', {'class': 'continue'}).get('href')
                    filtered_count = len(NetworkModule._filter_films(f'{NetworkModule._root_link}{list_url}', params))
            if (params.start_year is not None) | (params.end_year is not None):
                list_url = row.find('a', {'class': 'continue'}).get('href')
                filtered_count = len(NetworkModule._filter_films(f'{NetworkModule._root_link}{list_url}', params))
            if filtered_count < params.threshold:
                continue
            result.append(Relation(first=params.person, second=person, weight=filtered_count, params=params))
        return result
