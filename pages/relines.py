#!/usr/bin/python3
# -*- encoding=utf8 -*-
from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


class MainPage(WebPage):

    def __init__(self, web_driver, site_value, url=''):

        super().__init__(web_driver, site_value, url)

    # note main page
    search = WebElement(id='query')
    search_button = WebElement(xpath='//*[@id="searchBtn"]')
    products_list = ManyWebElements(
        xpath='//a[@class="product-list-item product-list-item_hover_active product-list-price-item__hover-wrapper"]')
    cart = WebElement(xpath='//a[@class="header__basket"]')
    car_brands = ManyWebElements(xpath='//a[@class="main-page-group__link"]')
    brand_name_h1 = WebElement(xpath='//h1[@class="catalog-header__title"]')

    # note cart
    item_cart = ManyWebElements(xpath='//*[@id="root"]/section/section/div/main/ul/li/section/a')

    # note product
    buy = WebElement(xpath='//button[@class="button button_big button_yellow product-info__button-buy"]')
