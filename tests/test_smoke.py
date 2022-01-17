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
def test_check_main_search(search, result, web_browser):
    """Проверяем поиск на главной странице."""

    with allure.step("Открываем главную страницу"):
        page = MainPage(web_browser)

    with allure.step(f'Вводим в поисковую строку "{search}"'):
        page.search = search
    with allure.step('Нажимаем кнопку "поиск"'):
        page.search_run_button.click()

    # Verify that user can see the list of products:
    with allure.step(f'проверяем что элементов "{result}"'):
        assert page.products_titles.count() == result


@allure.story('Тестирование корзины')
@pytest.mark.acceptance
def test_put_in_cart(web_browser):
    """Добавляем один элемент в корзину."""

    url = 'https://relines.ru/product/bolt-hexagon-flange-emvrq'
    with allure.step(f'Открываем страницу с товаром {url}'):
        page = MainPage(web_browser, url=url)

    with allure.step('Нажимаем кнопку купить'):
        page.pay.click()

    with allure.step('Переходим в корзину'):
        page.cart.click()

    with allure.step('Сравниваем что товар в карзине "1"'):
        assert page.item_cart.count() == 1

    with allure.step('Записываем куку для следующего теста'):
        write_cookies(page.get_cookies())



@allure.story('Тестирование корзины')
@pytest.mark.acceptance
def test_view_in_cart(web_browser):
    """Подкладываем куку и проверяем что есть 1 элемент в корзине."""

    url = 'https://relines.ru/cart'
    with allure.step(f"открываем страницу {url}"):
        page = MainPage(web_browser, url=url)

    with allure.step('загружаем куку и обновляем страницу'):
        page.add_cookie(read_cookies(), refresh=True)

    with allure.step("сравниваем количество товаров в корзине"):
        assert page.item_cart.count() == 1


@allure.feature('Другие')
@allure.story('Тестирование марок автомобилей')
@pytest.mark.smoke
def test_open_catalog(web_browser):
    """Прокликиваем Марки на главной странице."""

    with allure.step('Переходим на главную страницу'):
        page = MainPage(web_browser)

    for cat in page.main_categorys:
        group_name = cat.accessible_name
        with allure.step(f'Нажимаем на {group_name}'):
            cat.click()

        with allure.step(f'Проверяем, что в заголовке h1 содержится "{group_name}"'):
            assert group_name in page.name_category_h1.get_text()

        with allure.step(f'Проверяем, что в названии страницы есть "{group_name}"'):
            assert group_name in page.get_title()

        with allure.step('нажимаем назад'):
            page.go_back()