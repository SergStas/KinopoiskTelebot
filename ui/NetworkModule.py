import time
from threading import Thread

import requests
import random
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup


class RequestManager:
    _user_agents = None

    @staticmethod
    def _get_ip(session):
        ip = session.get('https://httpbin.org/ip').text.strip().split('"')[3]
        print(f'Current ip = {ip}')
        return ip

    @staticmethod
    def _next_proxy():
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="password")
            controller.signal(Signal.NEWNYM)
        time.sleep(1.5)
        print('Proxy switched')

    @staticmethod
    def _get_tor_session():
        result = requests.session()
        result.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        if RequestManager._user_agents is None:
            with open('user_agents.txt', 'r') as file:
                RequestManager._user_agents = file.read().strip().split('\n')
        agent = random.choice(RequestManager._user_agents)
        result.headers = {'User-agent': agent}
        print(f'Session created with user agent = {agent}')
        return result

    @staticmethod
    def proceed_request(url):
        start_time = None
        ip = None
        while True:
            try:
                session = RequestManager._get_tor_session()
                ip = RequestManager._get_ip(session)
                RequestManager._next_proxy()
                # session = NetworkModule._get_tor_session()
                # while ip == NetworkModule._get_ip(session):
                #     NetworkModule._next_proxy()
                #        session = NetworkModule._get_tor_session()
                start_time = time.time()
                html = session.get(url, timeout=5).text
                print(f'Response has been received with content length = {len(html)}, request url = {url}')
                return html
            except:
                print(f'\033[31mTimeout on session {ip} in {time.time() - start_time} sec\033[0m')


class NetworkModule:
    _root_link = 'https://www.kinopoisk.ru'
    _films_urls = []
    _captcha_cnt = 0

    @staticmethod
    def _get_films_from_rage(page):
        while True:
            try:
                html = RequestManager.proceed_request(f'{NetworkModule._root_link}/popular/films/?page={page}&tab=all')
                soup = BeautifulSoup(html, 'html.parser')
                films_list = soup.find('div', {'class': 'selection-list'})
                for url in films_list.find_all('a', {'class': 'selection-film-item-meta__link'}):
                    url = url.get('href')
                    NetworkModule._films_urls.append(f'{NetworkModule._root_link}{url}')
                break
            except:
                NetworkModule._captcha_cnt += 1
                print('\033[31mCaptcha detected!\033[0m')


    @staticmethod
    def _get_films_urls():
        threads = []
        for page in range(1, 21):
            thread = Thread(target=NetworkModule._get_films_from_rage, args=(page,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print(f'Films uploaded, captcha was thrown {NetworkModule._captcha_cnt} times')

    @staticmethod
    def _parse_film(url):
        while True:
            html = None
            try:
                html = RequestManager.proceed_request(url)
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.find('span', {'class': 'styles_title__2l0HH'}).text.split('(')[0].strip()
                year = soup.find('a', {'class': 'styles_linkLight__1Nxon styles_link__1N3S2'}).text.strip()
                # films_list = soup.find('div', {'class': 'selection-list'})
                # for url in films_list.find_all('a', {'class': 'selection-film-item-meta__link'}):
                #     url = url.get('href')
                #     NetworkModule._films_urls.append(f'{NetworkModule._root_link}{url}')
                print(f'Name = {name}, year = {year}')
                break
            except:
                NetworkModule._captcha_cnt += 1
                print('\033[31mCaptcha detected!\033[0m')
                print(f'Content length = {len(html)}')


    @staticmethod
    def load_data():
        NetworkModule._get_films_urls()
        # for url in NetworkModule._films_urls:
        #     NetworkModule._parse_film(url)
        return NetworkModule._films_urls


i = 0
start = time.time()
for film_url in NetworkModule.load_data():
    i += 1
    print(f'{i}. {film_url}')
print(f'Proceed in {time.time() - start} sec')
