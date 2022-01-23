"""Смок тесты."""
import allure
import pytest

from pages.relines import MainPage, get_test_data, CartPage


@allure.severity(allure.severity_level.BLOCKER)
@allure.story('Поиск')
@pytest.mark.smoke
@pytest.mark.parametrize('case', (
        ('normal_search'),
        ('bad_search'),
))
def test_check_main_search(case, web_browser, site_value, check_data_case):
    """Проверяем поиск на главной странице."""

    query, expected_result = check_data_case(get_test_data(site_value, case))

    with allure.step("'Переходим на главную страницу."):
        page = MainPage(web_browser, site_value)

    with allure.step(f'Вводим в поисковую строку "{query}".'):
        page.search = query
    with allure.step('Нажимаем кнопку "поиск".'):
        page.search_button.click()

    with allure.step(f'Проверяем что найдено товаров "{expected_result}".'):
        assert page.products_list.count() == expected_result


@allure.story('Тестирование корзины')
@pytest.mark.smoke
@pytest.mark.parametrize('case', (
        ('pay_product'),
))
def test_put_in_cart(case, web_browser, site_value, cookies_, check_data_case):
    """Добавляем один элемент в корзину."""

    url, expected_result = check_data_case(get_test_data(site_value, case))

    with allure.step(f'Открываем страницу с товаром {site_value + url}.'):
        page = CartPage(web_browser, site_value, url=url)

    with allure.step('Нажимаем кнопку купить.'):
        page.buy.click()

    with allure.step('Переходим в корзину.'):
        page.cart.click()

    with allure.step(f'Сравниваем что товар в карзине "{expected_result}".'):
        assert page.item_cart.count() == expected_result

    with allure.step('Записываем куку для следующего теста.'):
        cookies_(page.get_cookies())


@allure.story('Тестирование корзины')
@pytest.mark.smoke
@pytest.mark.parametrize('case', (
        ('pay_product'),
))
def test_view_in_cart(case, web_browser, site_value, cookies_, check_data_case):
    """Проверям что данные сохранились в сессии."""

    url, expected_result = check_data_case(get_test_data(site_value, case))

    with allure.step(f'Открываем страницу {site_value}.'):
        page = CartPage(web_browser, site_value)

    with allure.step('Загружаем куку от теста test_put_in_cart.'):
        page.add_cookie(cookies_())

    with allure.step('Нажимаем корзину.'):
        page.cart.click()

    with allure.step(f'Сравниваем количество товаров в корзине, должно быть {expected_result}.'):
        assert page.item_cart.count() == expected_result


@allure.feature('Другие')
@allure.story('Каталог марок автомобилей')
@pytest.mark.smoke
def test_open_catalog(web_browser, site_value):
    """Прокликиваем Марки на главной странице."""

    with allure.step('Переходим на главную страницу.'):
        page = MainPage(web_browser, site_value)

    for brand in page.car_brands:
        name = brand.accessible_name
        with allure.step(f'Нажимаем на {name}.'):
            brand.click()

        with allure.step(f'Проверяем, что в заголовке h1 содержится "{name}".'):
            assert name in page.brand_name_h1.get_text()

        with allure.step(f'Проверяем, что в названии страницы есть "{name}".'):
            assert name in page.get_title()

        with allure.step('Нажимаем назад.'):
            page.go_back()


@allure.severity(allure.severity_level.BLOCKER)
@allure.feature('Другие')
@allure.story('Главная страница')
@pytest.mark.smoke
def test_main_elements(web_browser, site_value):
    """Наличие всех элементов на странице."""

    important_elements = ['Relines', 'Каталог', 'Доставка', 'Контакты',
                          '+7 (495) 266-65-67', 'Оферта', 'Телеграм', 'Ватсап']
    count_important_elements = len(important_elements)

    with allure.step('Переходим на главную страницу.'):
        page = MainPage(web_browser, site_value)

    with allure.step(f'Количество важных элементов "{count_important_elements}".'):
        assert page.important_elements.count() == count_important_elements

    with allure.step(f'На странице имеются важные элементы {important_elements}.'):
        for element in page.important_elements.find():
            name = element.text or element.accessible_name
            assert name in important_elements


@allure.severity(allure.severity_level.BLOCKER)
@allure.story('Поиск')
@pytest.mark.smoke
@pytest.mark.xfail(reason='https://fat.relines.ru/browse/WEB-1610')
@allure.testcase('https://app.qase.io/project/WEBQ?view=1&suite=1&case=7&step=15', 'case, step 15')
@pytest.mark.parametrize('case', (
        ('brands_model_vendor_1'),
))
def test_search_brandart(case, web_browser, site_value, check_data_case):
    """Поиск по марке/модели и артикулу"""

    _brand, _model, _vendor_code = check_data_case(get_test_data(site_value, case))

    with allure.step('Переходим на главную страницу.'):
        page = MainPage(web_browser, site_value)

    with allure.step('Нажимаем в строку поиск.'):
        page.search.click()

    with allure.step('Нажимаем меню "Все марки".'):
        page.search_brands_menu.click()

    with allure.step(f'Выбираем марку "{_brand}" модель "{_model}".'):
        for brand in page.brands_menu_brands:
            if _brand in brand.text:
                brand.click()
                for model in page.brands_menu_models:
                    if _model in model.text:
                        model.click()

    with allure.step(f'Вводим в поисковую строку "{_vendor_code}".'):
        page.search = _vendor_code

    with allure.step('Нажимаем кнопку "поиск".'):
        page.search_button.click()

    with allure.step('Проверяем что найдены детали.'):
        assert 'Ничего не найдено' not in page.not_found.get_text()
        assert page.products_list.count()
