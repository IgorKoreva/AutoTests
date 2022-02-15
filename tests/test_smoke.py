"""Смок тесты."""
import time

import allure
import pytest

from pages.relines import MainPage, get_test_data, CartPage, _get_elem_accessible_name, _get_elem_text


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
    # todo 9. Убавляем оставшиеся товары
    #  10. Проверяем, что в корзине пусто

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


@allure.severity(allure.severity_level.NORMAL)
@allure.story('Каталог')
@pytest.mark.smoke
@pytest.mark.parametrize('case', (
        ('breadcrumbs'),
        ('breadcrumbs1'),
))
def test_breadcrumbs(case, check_data_case, web_browser, site_value):
    """Переходы по хлебным крошкам."""

    with allure.step('Переходим на главную страницу'):
        page = MainPage(web_browser, site_value)

    mark, model, cat, b_crumbs = check_data_case(get_test_data(site_value, case))


    with allure.step(f'Нажимаем на "{mark}".'):
        _get_elem_accessible_name(page.car_brands, mark).click()

    with allure.step(f'Нажимаем на "{model}".'):
        _get_elem_accessible_name(page.car_models, model).click()

    for search in cat:
        with allure.step(f'Нажимаем на "{search}".'):
            _get_elem_accessible_name(page.cat_dir, search).click()
            time.sleep(1)

    for search in b_crumbs:
        with allure.step(f'Нажимаем в хлебных крошках "{search}".'):
            _get_elem_text(page.bread_crumbs, search).click()
            time.sleep(0.5)
            with allure.step(f'Проверяем что в заголовке страницы содержится "{search}".'):
                assert search in page.get_title()
            with allure.step(f'Проверяем, что в заголовке h1 содержится "{search}".'):
                assert search in page.brand_name_h1.get_text()


@allure.story('Тестирование корзины')
@pytest.mark.smoke
@pytest.mark.parametrize('case', (
        ('add_del_cart'),
))
def test_add_del_cart(case, check_data_case, web_browser, site_value):
    """Добавляем и удаляем элементы из корзины."""

    url, details = check_data_case(get_test_data(site_value, case))

    with allure.step(f'Переходим в каталог с товаром {site_value + url}.'):
        page = CartPage(web_browser, site_value, url=url)

    for detail in details:
        with allure.step(f'Нажимаем на деталь "{detail}".'):
            _get_elem_text(page.products_not_incart, detail).click()
        with allure.step(f'Нажимаем купить'):
            page.buy.click()
        with allure.step(f'Нажимаем назад'):
            page.go_back()

    with allure.step(f'Нажимаем корзину'):
        page.cart.click()
    count = 1
    with allure.step(f'Добавляем 1 шт. к первому товару.'):
        page.add_product[0].click()
        count += 1
        time.sleep(0.5)
    with allure.step(f'Проверяем товар добавился'):
        assert page.count_product[0].text == f'{count} шт.'

    for element in [page.del_product, page.del_product]:
        with allure.step(f'Убавляем 1 шт. у первого товара.'):
            element[0].click()
            count -= 1
        if count > 0:
            with allure.step(f'Проверяем товар убавился'):
                time.sleep(0.5)
                assert page.count_product[0].text == f'{count} шт.'
        else:
            with allure.step(f'Проверяем товар удалился из корзины, и в корзине остался 1 товар'):
                time.sleep(0.5)
                assert page.item_cart.count() < len(details)

@allure.story('Тестирование сумм и количества товаров в корзине')
@pytest.mark.smoke
@pytest.mark.parametrize('case', (
        ('sum_add_del_cart'),
))
def test_sum_add_del_cart(case, check_data_case, web_browser, site_value):
    """Проверяем сумму и количество товара в корзине."""

    url = check_data_case(get_test_data(site_value, case))

    with allure.step(f'Переходим в каталог с товаром {site_value + url}.'):
        page = CartPage(web_browser, site_value, url=url)
    time.sleep(1)

    with allure.step(f'Находим деталь Болт м6х14 и нажимаем "Ориг. $$$ Р". Одна деталь попадает в корзину.'):
        page.bolt_orig.click()
        time.sleep(1)

    with allure.step(f'Извлекаем цену и количество деталей Болт м6х14, помещенных в корзину.'):
        ceni = []
        for price in page.boltprice:
            ceni.append(price.text)
        cena = int(ceni[0])

        for qua in page.quantity:
            kolich = int(qua.text)

    with allure.step(f'Переходим к корзину. Клик по корзине.'):
        page.cart.click()

    with allure.step(f'Извлекаем сумму отображенную на товаре'):
        prices_on_prodincart = []
        for price_onprod in page.sum_on_prodincart:
            prices_on_prodincart.append(price_onprod.text)
        price_on_prodincart = int(prices_on_prodincart[0])

    with allure.step(f'Извлекаем количество товара отображенное на товаре'):
        for quan_onprod in page.quan_on_prodincart:
            qu = (quan_onprod.text).split()
        quantity_onprod = int(qu[0])

    with allure.step(f'Извлекаем сумму, отображенную на желтой кнопке "Оформить заказ на $$$ Р"'):
        prices_yellow = []
        for price_y in page.sum_yellow_button:
            prices_yellow.append(price_y.text)
        price_yellow = int(prices_yellow[0])

    with allure.step(f'Извлекаем сумму, отображенную на красной кнопке "Корзина"'):
        prices_red = []
        for price_r in page.sum_red_button:
            prices_red.append(price_r.text)
        price_red = int(prices_red[0])

    with allure.step(f'Проверяем, что сумма везде одинаковая = {cena} Р'):
        assert cena*kolich == price_yellow == price_red == price_on_prodincart




