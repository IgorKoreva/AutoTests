import json

import allure
import pytest

from pages.base import write_cookies, read_cookies
from pages.relines import MainPage


@allure.severity(allure.severity_level.BLOCKER)
@allure.story('Тестирование поиска')
@pytest.mark.smoke
@pytest.mark.parametrize('search, result', (
        ('Chery Fora Мотор стеклоочистителя', 2),
        ('Chery Fora Мотор стеклооddsadsasdчистителя', 0),
))
def test_check_main_search(search, result, web_browser, site_value):
    """Проверяем поиск на главной странице."""

    with allure.step("Открываем главную страницу"):
        page = MainPage(web_browser, site_value)

    with allure.step(f'Вводим в поисковую строку "{search}"'):
        page.search = search
    with allure.step('Нажимаем кнопку "поиск"'):
        page.search_button.click()

    # Verify that user can see the list of products:
    with allure.step(f'проверяем что элементов "{result}"'):
        assert page.products_list.count() == result


@allure.story('Тестирование корзины')
@pytest.mark.acceptance
def test_put_in_cart(web_browser, site_value):
    """Добавляем один элемент в корзину."""

    url = 'product/bolt-hexagon-flange-emvrq'
    with allure.step(f'Открываем страницу с товаром {site_value + url}'):
        page = MainPage(web_browser, site_value, url=url)

    with allure.step('Нажимаем кнопку купить'):
        page.buy.click()

    with allure.step('Переходим в корзину'):
        page.cart.click()

    with allure.step('Сравниваем что товар в карзине "1"'):
        assert page.item_cart.count() == 1

    with allure.step('Записываем куку для следующего теста'):
        write_cookies(page.get_cookies())



@allure.story('Тестирование корзины')
@pytest.mark.acceptance
def test_view_in_cart(web_browser, site_value):
    """Подкладываем куку и проверяем что есть 1 элемент в корзине."""

    url = 'cart'
    with allure.step(f"открываем страницу {site_value + url}"):
        page = MainPage(web_browser, site_value, url=url)

    with allure.step('загружаем куку и обновляем страницу'):
        page.add_cookie(read_cookies(), refresh=True)

    with allure.step("сравниваем количество товаров в корзине"):
        assert page.item_cart.count() == 1


@allure.feature('Другие')
@allure.story('Тестирование марок автомобилей')
@pytest.mark.smoke
def test_open_catalog(web_browser, site_value):
    """Прокликиваем Марки на главной странице."""

    with allure.step('Переходим на главную страницу'):
        page = MainPage(web_browser, site_value)

    for brand in page.car_brands:
        name = brand.accessible_name
        with allure.step(f'Нажимаем на {name}'):
            brand.click()

        with allure.step(f'Проверяем, что в заголовке h1 содержится "{name}"'):
            assert name in page.brand_name_h1.get_text()

        with allure.step(f'Проверяем, что в названии страницы есть "{name}"'):
            assert name in page.get_title()

        with allure.step('нажимаем назад'):
            page.go_back()