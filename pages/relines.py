#!/usr/bin/python3
# -*- encoding=utf8 -*-
import json
import os

from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


class MainPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or 'https://relines.ru/'

        super().__init__(web_driver, url)

    # Main search field
    search = WebElement(id='query')
    search_run_button = WebElement(xpath='//*[@id="searchBtn"]')
    products_titles = ManyWebElements(xpath='//*[@id="root"]/section/section/section/section/section/section/a')

    # Button to sort products by price
    sort_products_by_price = WebElement(css_selector='button[data-autotest-id="dprice"]')

    # Prices of the products in search results
    products_prices = ManyWebElements(xpath='//div[@data-zone-name="price"]//span/*[1]')

    pay = WebElement(xpath='//*[@id="root"]/section/section/section/section/main/section/section[4]/section/button')
    cart = WebElement(xpath='//*[@id="root"]/section/header/section/section[2]/section[2]/a[2]/div')
    item_cart = ManyWebElements(xpath='//*[@id="root"]/section/section/div/main/ul/li/section/a')

    # note: category
    main_categories = ManyWebElements(xpath='//a[@class="main-page-group__link"]')
    name_category_h1 = WebElement(xpath='//h1[@class="catalog-header__title"]')