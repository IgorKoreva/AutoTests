#!/usr/bin/python3
# -*- encoding=utf8 -*-

import pytest
import allure
import uuid

from allure_commons.types import AttachmentType


def pytest_make_parametrize_id(config, val):
    """Для поддержки кириллицы в тестах."""
    return repr(val)


def pytest_addoption(parser):
    """Параметры."""
    parser.addoption("--site", action="store", default='https://relines.ru/', type=str, help="site, http://127.0.0.1/")


@pytest.fixture
def site_value(request):
    param = request.config.getoption("--site")
    return param + '/' if param[-1] != '/' else param


@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')
    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    yield browser

    if request.node.rep_call.failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            screen = str(uuid.uuid4()) + '.png'
            browser.save_screenshot('screenshots/' + screen)

            allure.attach(browser.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=AttachmentType.PNG)

            attach = browser.get_screenshot_as_png()
            allure.attach(request.function.__name__, attach, allure.attach_type.PNG)

            print('URL: ', browser.current_url)
            print('Browser logs:')
            print('local screen: ', './screenshots/' + screen)
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass
