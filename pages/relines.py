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
    chery = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[1]/a')
    geely = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[2]/a')
    great_wall = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[3]/a')
    haval = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[4]/a')
    lifan = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[5]/a')
    vortex = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[6]/a')
    byd = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[7]/a')
    changan = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[8]/a')
    brilliance = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[9]/a')
    faw = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[10]/a')
    dfm = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[11]/a')
    foton = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[12]/a')
    howo = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[13]/a')
    shacman = WebElement(xpath=f'//*[@id="root"]/section/section/main/section/div[2]/section[14]/a')
    category_name = WebElement(xpath='//*[@id="root"]/section/section/main/section[1]/section[2]/header/h1')