#!/usr/bin/python3
# -*- encoding=utf8 -*-
"""Модуль с сайтом."""

import json

from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


def read_test_data():
    """Чтение файла."""
    with open('test_data.json', mode='r', encoding='utf-8') as f:
        return json.load(f)
    return {}


def _get_elem_accessible_name(elements: ManyWebElements, name: str) -> WebElement:
    for el in elements:
        if name in el.accessible_name:
            return el


def _get_elem_text(elements: ManyWebElements, text: str) -> WebElement:
    for el in elements:
        if text in el.text:
            return el


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
    car_models = ManyWebElements(xpath='//a[@class="category-page-car-model category-page-car-model_hover_active '
                                       'category-page-car-model_focus_active category-page-car-models__category"]')
    cat_dir = ManyWebElements(xpath='//a[@class="category-page-subcategories__section-link"]')
    bread_crumbs = ManyWebElements(xpath='//a[@class="link breadcrumbs__link"]')
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
    products_not_incart = ManyWebElements(xpath='//h2[@class="typography__root typography__body typography '
                                                'typography_color_primary product-list-item__name"]')
    products_incart = ManyWebElements(xpath='//button[@class="button product-list-price-item '
                                            'product-list-price-item_border_dark product-list-prices__item"]')
    add_product = ManyWebElements(xpath='//button[@class="button basket-product__increase-button"]')
    del_product = ManyWebElements(xpath='//button[@class="button"]')
    count_product = ManyWebElements(xpath='//p[@class="typography__root typography__body typography '
                                          'basket-product__quantity"]')
    # Кнопка "Ориг." - добавляет деталь в корзину
    bolt_orig = WebElement(xpath='//a[@href="/product/bolt-m6kh14-mpng"]//*[contains(text(), "Ориг.")]')
    # цена, указанная за деталь в каталоге "Ориг." тут "181 Р"
    boltprice = ManyWebElements(xpath='//a[@href="/product/bolt-m6kh14-mpng"]//span[@class="currency-label"]//span')
    # количество деталей отображенных в красном кружке в каталоге
    quantity = ManyWebElements(xpath='//a[@href="/product/bolt-m6kh14-mpng"]//div[@class="badge '
                                     'product-list-price-item__badge"]')
    # Сумма на желтой кнопке "Оформить заказ" в корзине
    sum_yellow_button = ManyWebElements(xpath='//*[text()="Оформить заказ на "]//span[@class="currency-label"]//span')
    # Сумма на товаре в корзине
    sum_on_prodincart = ManyWebElements(xpath='//*[text()="Болт м6х14"]/../../..//span[@class="currency-label"]//span')
    # Количество товара на товаре в корзине
    quan_on_prodincart = ManyWebElements(xpath='//*[text()="Болт м6х14"]/../../..//p[@class="typography__root '
                                               'typography__body typography basket-product__quantity"]')
    # Сумма на красной кнопке "Корзина"
    sum_red_button = ManyWebElements(xpath='//span[@class="currency-label basket-link-btn__price"]//span')


