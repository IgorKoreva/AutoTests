import json
import time

import allure
import pytest

from pages.base import write_cookies, read_cookies
from pages.relines import MainPage, get_const


@allure.severity(allure.severity_level.BLOCKER)
@allure.story('Поиск')
@pytest.mark.smoke
def test_check_main_search(web_browser, site_value):
    """Проверяем поиск на главной странице."""
    const = get_const(site_value)
    for search, count in const['search']:
        with allure.step("Открываем главную страницу"):
            page = MainPage(web_browser, site_value)

        with allure.step(f'Вводим в поисковую строку "{search}"'):
            page.search = search
        with allure.step('Нажимаем кнопку "поиск"'):
            page.search_button.click()

        with allure.step(f'проверяем что элементов "{count}"'):
            assert page.products_list.count() == count


@allure.story('Тестирование корзины')
@pytest.mark.smoke
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
@pytest.mark.smoke
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


@allure.severity(allure.severity_level.BLOCKER)
@allure.feature('Другие')
@allure.story('Главная старница')
@pytest.mark.smoke
def test_main_elements(web_browser, site_value):
    """Наличие всех элементов на странице."""

    with allure.step('Переходим на главную страницу'):
        page = MainPage(web_browser, site_value)

    with allure.step('Проверяем что на странице есть 9 элементов[лого, Каталог, Доставка, Контакты, телефон, оферта, телеграм, васап]'):
        assert page.elements.count() == 9


@allure.severity(allure.severity_level.BLOCKER)
@allure.story('Поиск')
@pytest.mark.underconstruction
@pytest.mark.xfail(reason='https://fat.relines.ru/browse/WEB-1610')
@allure.testcase('https://app.qase.io/project/WEBQ?view=1&suite=1&case=7&step=15', 'кейс, шаг 15')
def test_search_brandart(web_browser, site_value):
    """Поиск по марке/модели и артикулу"""

    const = get_const(site_value)

    for _brand, _model, _vendor_code in const['brands']:
        with allure.step('Переходим на главную страницу'):
            page = MainPage(web_browser, site_value)

        with allure.step('Щелкаем в строку поиск'):
            page.search.click()

        with allure.step('Нажимаем меню "Все марки"'):
            page.search_brands_menu.click()

        with allure.step(f'Выбираем марку "{_brand}" модель "{_model}"'):
            for brand in page.brands_menu_brands:
                if _brand in brand.text:
                    brand.click()
                    for model in page.brands_menu_models:
                        if _model in model.text:
                            model.click()

        with allure.step(f'Вводим в поисковую строку "{_vendor_code}"'):
            page.search = _vendor_code

        with allure.step('Нажимаем кнопку "поиск"'):
            page.search_button.click()

        with allure.step('Проверяем что найдена деталь'):
            assert 'Ничего не найдено' != page.not_found.get_text()
            assert 0 < page.products_list.count()


# @pytest.mark.underconstruction
# def test_