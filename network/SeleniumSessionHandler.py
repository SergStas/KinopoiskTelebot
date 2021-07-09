import time

from selenium import webdriver


class SeleniumSessionHandler:
    _root_link = "https://www.kinopoisk.ru"

    @staticmethod
    def get_search_response(driver, name):
        label2 = "kinopoisk-header-search-form-input__input"
        find = "search-form-submit-button__icon"
        show_all = ".//a[contains(text(),'показать')]"
        driver.find_element_by_class_name(label2).send_keys(name)
        driver.find_element_by_class_name(find).click()
        driver.find_element_by_xpath(show_all).click()
        return driver.page_source

    @staticmethod
    def _yandex_authorization(driver, login, password):
        driver.find_element_by_id("passp-field-login").send_keys(login)
        driver.find_element_by_css_selector("button.Button2").click()
        time.sleep(0.3)
        driver.find_element_by_id("passp-field-passwd").send_keys(password)
        driver.find_element_by_css_selector("button.Button2").click()

    @staticmethod
    def _join_for_driver(driver, login, password):
        css_selector = "button._3upCsVwB8ncX5nAFH7QnPq"
        driver.find_element_by_css_selector(css_selector).click()
        SeleniumSessionHandler._yandex_authorization(driver, login, password)

    @staticmethod
    def get_session():
        driver = webdriver.Firefox()
        driver.get(SeleniumSessionHandler._root_link)
        with open('../security.txt', 'r') as file:
            content = file.read()
            login = [row for row in content.split('\n') if len(row.split('login=')) == 2][0].split('login=')[1]
            password = [row for row in content.split('\n') if len(row.split('password=')) == 2][0].split('password=')[1]
        SeleniumSessionHandler\
            ._join_for_driver(driver, login, password)
        return driver


dr = SeleniumSessionHandler.get_session().get(SeleniumSessionHandler._root_link)
