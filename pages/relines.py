#!/usr/bin/python3
# -*- encoding=utf8 -*-
from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


def get_const(site):
    const_dict = {
        'https://relines.ru/': {
            'search': (('Chery Fora Мотор стеклоочистителя', 2),
                       ('Chery Fora Мотор стеклооddsadsasdчистителя', 0)),
            'brands': [('Great Wall', 'Sailor', '2804200-B00')],
        },
        'https://stg.relines.ru/': {
            'search': (('Chery Fora Мотор стеклоочистителя', 2),
                       ('Chery Fora Мотор стеклооddsadsasdчистителя', 0)),
            'brands': (('Great Wall', 'Sailor', '2804200-B00'),
                       ('Faw', 'Besturn B50', '2804200-B00')),
        }
    }
    return const_dict[site]


class MainPage(WebPage):

    def __init__(self, web_driver, site_value, url=''):

        super().__init__(web_driver, site_value, url)

    # note main page
    search = WebElement(id='query')
    search_button = WebElement(xpath='//*[@id="searchBtn"]')
    search_brands_menu = WebElement(id='searchMenuBtn')
    products_list = ManyWebElements(
        xpath='//a[@class="product-list-item product-list-item_hover_active product-list-price-item__hover-wrapper"]')
    cart = WebElement(xpath='//a[@class="header__basket"]')
    brands_menu_brands = ManyWebElements(xpath='//*[@id="searchMenu"]/div/ul/li[*]/div')
    brands_menu_models = ManyWebElements(xpath='//*[@id="searchMenu"]/div/ul/li[*]/ul/li')

    car_brands = ManyWebElements(xpath='//a[@class="main-page-group__link"]')
    brand_name_h1 = WebElement(xpath='//h1[@class="catalog-header__title"]')
    elements = ManyWebElements(xpath='//a[contains(@class, "link header-nav__link") or ' \
                                     'contains(@class, "header__logo") or ' \
                                     'contains(@class, "link footer__menu-link") or ' \
                                     'contains(@class, "link footer-messengers__messenger") or ' \
                                     'contains(@class, "link header__phone") and ' \
                                     '@class!="link header__phone-mobile hidden-md hidden-lg"]')

    # note cart
    item_cart = ManyWebElements(xpath='//*[@id="root"]/section/section/div/main/ul/li/section/a')

    # note product
    buy = WebElement(xpath='//button[@class="button button_big button_yellow product-info__button-buy"]')
    not_found = WebElement(xpath='//h5[@class="search-page-no-results__text-typography"]')
