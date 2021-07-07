import time
from bs4 import BeautifulSoup

from models.dataclasses.Params import Params
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
    def get_actors(driver, params):
        time.sleep(3)
        html = SeleniumSessionHandler.get_search_response(driver, params)
        soup = BeautifulSoup(html, 'html.parser')
        hrefs = soup.find_all('a', {'data-type': 'person'})
        urls = []
        for e in hrefs:
            link = e.get('data-url')
            urls.append(f'{NetworkModule._root_link}{link}')

        def predicate(link_to_check):
            return len(link_to_check.split('/')) == 5

        urls = list(set(list(filter(predicate, urls))))
        result = []
        for url in urls:
            result.append(NetworkModule._parse_person(driver, url))
        return result

    @staticmethod
    def _get_only_actors_rows(rows):
        result = []
        first_time = False
        for row in rows:
            # print(list(row.children))
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
    def _check_film(url, genres):
        html = RequestManager.request(url)
        soup = BeautifulSoup(html, 'html.parser')
        actual_genres = [i.text for i in [e for e in soup.find_all('a') if e.get('href') is not None]
                         if (len(i.get('href').split('navigator')) == 2) & (len(i.get('href').split('country')) == 1) &
                         (len([int(s) for s in i.get('href').split('/') if s.isdigit()]) == 0)]
        for genre in genres:
            if genre.lower() in [s.lower() for s in actual_genres]:
                return True
        return False

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
                         [e.get('href') for e in item.find_all('a') if len(e.get('href').split('votes')) == 1]]:
                result.append(film)
        return [i for i in result if NetworkModule._check_film(i, params.genres)]

    @staticmethod
    def get_relations(params):
        html = RequestManager.request(f'{NetworkModule._root_link}/name/{params.person.person_id}/relations/')
        soup = BeautifulSoup(html, 'html.parser')
        rows = [e for e in [a.parent.parent for a in soup.find_all('a')
                            if len(a.text.split('фильмов:')) == 2]
                if params.threshold <= int(e.text.split('фильмов: ')[1].split('.')[0])]
        if params.actors_only:
            rows = NetworkModule._get_only_actors_rows(rows)
        result = []
        for row in rows:
            count = int(row.text.split('фильмов: ')[1].split('.')[0])
            filtered_count = count
            if params.genres is not None:
                if len(params.genres) != 0:
                    list_url = row.find('a', {'class': 'continue'}).get('href')
                    filtered_count = len(NetworkModule._filter_films(f'{NetworkModule._root_link}{list_url}', params))
            if filtered_count < params.threshold:
                continue
            person_url = row.find('a').get('href')
            person = NetworkModule \
                ._parse_person(RequestManager.get_current_session(), f'{NetworkModule._root_link}{person_url}')
            result.append(Relation(first=params.person, second=person, weight=filtered_count, params=params))
        return result


start = time.time()
NetworkModule.get_relations(Params(threshold=15, actors_only=True, genres=['криминал'],
                                   end_year=None, start_year=None, rank=None, generate_gif=None, name=None,
                                   person=Person(person_id=513, url=None, full_name=None)))
print(f'Proceed in {time.time() - start} sec')
