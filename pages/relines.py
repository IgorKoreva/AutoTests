#!/usr/bin/python3
# -*- encoding=utf8 -*-
"""Модуль с сайтом."""

import json

from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


def read_test_data():
    """Чтение файла"""
    with open('test_data.json', mode='r', encoding='utf-8') as f:
        return json.load(f)
    return {}


SUIT_CASE = read_test_data()


def get_test_data(site, case):
    """Получение данных по названию кейса."""
    return SUIT_CASE[site].get(case, None)


class MainPage(WebPage):
    """Главная страница."""

    def __init__(self, web_driver, site_value, url=''):
        super().__init__(web_driver, site_value, url)

    search = WebElement(id='query')
    search_button = WebElement(xpath='//*[@id="searchBtn"]')
    search_brands_menu = WebElement(id='searchMenuBtn')
    products_list = ManyWebElements(
        xpath='//a[@class="product-list-item product-list-item_hover_active product-list-price-item__hover-wrapper"]')
    brands_menu_brands = ManyWebElements(xpath='//*[@id="searchMenu"]/div/ul/li[*]/div')
    brands_menu_models = ManyWebElements(xpath='//*[@id="searchMenu"]/div/ul/li[*]/ul/li')

    car_brands = ManyWebElements(xpath='//a[@class="main-page-group__link"]')
    brand_name_h1 = WebElement(xpath='//h1[@class="catalog-header__title"]')
    important_elements = ManyWebElements(xpath='//a[contains(@class, "link header-nav__link") or ' \
                                               'contains(@class, "header__logo") or ' \
                                               'contains(@class, "link footer__menu-link") or ' \
                                               'contains(@class, "link footer-messengers__messenger") or ' \
                                               'contains(@class, "link header__phone") and ' \
                                               '@class!="link header__phone-mobile hidden-md hidden-lg"]')
    not_found = WebElement(xpath='//h5[@class="search-page-no-results__text-typography"]')


class CartPage(WebPage):
    """Страница с корзиной."""

    def __init__(self, web_driver, site_value, url=''):
        super().__init__(web_driver, site_value, url)

    cart = WebElement(xpath='//a[@class="header__basket"]')
    item_cart = ManyWebElements(xpath='//*[@id="root"]/section/section/div/main/ul/li/section/a')
    buy = WebElement(xpath='//button[@class="button button_big button_yellow product-info__button-buy"]')
    not_found = WebElement(xpath='//h5[@class="search-page-no-results__text-typography"]')
