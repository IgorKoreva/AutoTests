import json

import allure
import pytest

from pages.base import write_cookies, read_cookies
from pages.relines import MainPage


@allure.severity(allure.severity_level.BLOCKER)
@allure.story('Смоки-хуеки первый тест')
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


@allure.story('Смоки-хуеки второй тест')
@pytest.mark.smoke
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


@allure.feature('фича-хуича')
@allure.story('Смоки-хуеки третий тест')
@pytest.mark.smoke
def test_view_in_cart(web_browser):
    """Подкладываем куку и проверяем что есть 1 элемент в корзине."""

    url = 'https://relines.ru/cart'
    with allure.step(f"открываем страницу {url}"):
        page = MainPage(web_browser, url=url)

    with allure.step('загружаем куку и обновляем страницу'):
        page.add_cookie(read_cookies(), refresh=True)

    with allure.step("сравниваем количество товаров в корзине"):
        assert page.item_cart.count() == 1


@pytest.mark.smoke
def test_open_catalog(web_browser):
    """Прокликиваем Марки на главной странице."""

    with allure.step('Переходим на главную страницу'):
        page = MainPage(web_browser)

    cat_list = [(page.chery.click, 'Chery'),
                (page.geely.click, 'Geely'),
                (page.great_wall.click, 'Great Wall'),
                (page.haval.click, 'Haval'),
                (page.lifan.click, 'Lifan'),
                (page.vortex.click, 'Vortex'),
                (page.byd.click, 'Byd'),
                (page.changan.click, 'Changan'),
                (page.brilliance.click, 'Brilliance'),
                (page.faw.click, 'Faw'),
                (page.dfm.click, 'Dongfeng'),
                (page.foton.click, 'Foton'),
                (page.howo.click, 'Howo'),
                (page.shacman.click, 'Shacman'),
                ]

    for click, name in cat_list:
        with allure.step(f'Нажимаем на {name}'):
            click()

        with allure.step(f'Проверяем, что в заголовке h1 содержится "{name}"'):
            assert name in page.category_name.get_text()

        with allure.step(f'Проверяем, что в названии страницы есть "{name}"'):
            assert name in page.get_title()

        with allure.step('нажимаем назад'):
            page.go_back()


