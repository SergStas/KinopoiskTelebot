import time

from selenium import webdriver  # D:\anaconda\Scripts\pip.exe install selenium
# from selenium.webdriver.common.keys import Keys  # Устанавливаем клавиши, чтобы на фортепьяно можно было игратт
# from bs4 import BeautifulSoup  # комментарии излишни
# import time


# vzlomzhepy120421@yandex.ru
# bronetemkinponosec


class SeleniumSessionHandler:  # Запрос в строку кинопоиска, лабель метки такой: <input type="text" name="kp_query"
    # class="_3PYIxv6wCqArZwY93wQ_Jt ddZaLwoP17d6om4TLZSxm kinopoisk-header-search-form-input__input"
    # autocomplete="off" aria-label="Фильмы, сериалы, персоны" placeholder="Фильмы, сериалы, персоны" value=""
    # required="">
    _root_link = "https://www.kinopoisk.ru"
    _kp_login = "vzlomzhepy120421"
    _kp_password = "bronetemkinponosec"

    @staticmethod
    def get_search_response(driver, params):
        # Работа с селеном, запрос самому селену, используется в self.create_response()
        label2 = "kinopoisk-header-search-form-input__input"
        find = "search-form-submit-button__icon"
        show_all = ".//a[contains(text(),'показать')]"
        driver.find_element_by_class_name(label2).send_keys(params.name)  # пишем заброс поиску кинопоиска
        driver.find_element_by_class_name(find).click()
        driver.find_element_by_xpath(show_all).click()
        return driver.page_source

    @staticmethod
    def _yandex_authorization(driver, login, password):  # Штурмуем яндекс авторизацию, используется в join_for_driver()
        driver.find_element_by_id("passp-field-login").send_keys(login)
        driver.find_element_by_css_selector("button.Button2").click()
        time.sleep(0.3)
        driver.find_element_by_id("passp-field-passwd").send_keys(password)
        driver.find_element_by_css_selector("button.Button2").click()

    @staticmethod
    def _join_for_driver(driver, login, password):
        css_selector = "button._3upCsVwB8ncX5nAFH7QnPq"
        # Скорее всего сайт жопится, потому что мы не зареганы, на всякий случай попробуем
        # css_selector - кнопка войти на кинопоиске, если эта поменяет за ночь класс, будет печально, но не критично
        driver.find_element_by_css_selector(css_selector).click()
        SeleniumSessionHandler._yandex_authorization(driver, login, password)

    @staticmethod
    def get_session():
        driver = webdriver.Firefox()
        driver.get(SeleniumSessionHandler._root_link)
        SeleniumSessionHandler\
            ._join_for_driver(driver, SeleniumSessionHandler._kp_login, SeleniumSessionHandler._kp_password)
        return driver


# driver = webdriver.Firefox()  # Кладем дрявер в папку с проектом, подробнее: geckodriver для selenium
# driver.get("https://www.kinopoisk.ru")  # Наша ссылка
#
# kp_login = "vzlomzhepy120421"  # комментарии излишни
# kp_password = "bronetemkinponosec"  # комментарии излишни


# join_for_driver(login, password)
# dr = SeleniumSessionHandler.get_session()
# SeleniumSessionHandler.get_actors(dr, 'Уилл Смитт')
