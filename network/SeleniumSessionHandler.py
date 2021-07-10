import time

from selenium import webdriver
from threading import current_thread


class SeleniumSessionHandler:
    _root_link = "https://www.kinopoisk.ru"
    _sessions = {}

    @staticmethod
    def get_search_response(driver, name):
        driver.get(SeleniumSessionHandler._root_link)
        label2 = "kinopoisk-header-search-form-input__input"
        find = "search-form-submit-button__icon"
        show_all = ".//a[contains(text(),'показать')]"
        driver.find_element_by_class_name(label2).send_keys(name)
        driver.find_element_by_class_name(find).click()
        # driver.find_element_by_xpath(show_all).click()
        return driver.page_source

    @staticmethod
    def _yandex_authorization(driver, login, password):
        driver.find_element_by_id("passp-field-login").send_keys(login)
        driver.find_element_by_css_selector("button.Button2").click()
        time.sleep(0.3)
        driver.find_element_by_id("passp-field-passwd").send_keys(password)
        driver.find_element_by_css_selector("button.Button2").click()
        time.sleep(3)

    @staticmethod
    def _join_for_driver(driver, login, password):
        css_selector = "button._3upCsVwB8ncX5nAFH7QnPq"
        driver.find_element_by_css_selector(css_selector).click()
        SeleniumSessionHandler._yandex_authorization(driver, login, password)

    @staticmethod
    def get_session():
        try:
            return SeleniumSessionHandler._sessions[current_thread().name]
        except:
            driver = webdriver.Firefox()
            SeleniumSessionHandler._sessions[current_thread().name] = driver
            print(f'Session for thread {current_thread().name} has been inited')
            driver.get(SeleniumSessionHandler._root_link)
            with open('security.txt', 'r') as file:
                content = file.read()
                login = [row for row in content.split('\n') if len(row.split('login=')) == 2][0].split('login=')[1]
                password = [row for row in content.split('\n') if len(row.split('password=')) == 2][0].split('password=')[1]
            SeleniumSessionHandler\
                ._join_for_driver(driver, login, password)
            return driver
