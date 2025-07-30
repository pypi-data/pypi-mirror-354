import unittest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium_crawler.scraping_tools import get_clickable_element, get_element
from selenium_crawler.webdrivercreator import create_webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class TestIntegrationScrapingTools(unittest.TestCase):

    def test_get_element(self):
        driver = None
        try:
            driver = create_webdriver()
            driver.get("https://github.com/jo-hoe/selenium-crawler")

            element = get_element(
                driver, (By.XPATH, "//a[text()='selenium-crawler']"))

            assert element is not None, "Element not found on the page"
        except TimeoutException:
            assert False, "Element not found within the timeout period."
        finally:
            if driver:
                driver.quit()

    def test_get_clickable_button(self):
        driver = None
        try:
            driver = create_webdriver()
            driver.get("https://github.com/jo-hoe/selenium-crawler")

            element = get_clickable_element(
                driver, (By.XPATH, "//button[contains(@class, 'prc-Button-ButtonBase')]"))

            assert element is not None, "Element not found on the page"
        finally:
            if driver:
                driver.quit()

    def assert_test(self, driver: WebDriver, locator: tuple[str, str]) -> None:
        try:
            elements = get_element(driver, locator)
            # check if element has a class attribute that contains 'passed'
            attribute = elements.get_attribute('class')
            if attribute == 'result passed' or attribute == 'passed':
                assert True
            else:
                assert False, (
                    f"element {locator[1]} found but does not have the expected class: {attribute}")
        except TimeoutException:
            assert False, f"element {locator[1]} not found within the timeout period."
