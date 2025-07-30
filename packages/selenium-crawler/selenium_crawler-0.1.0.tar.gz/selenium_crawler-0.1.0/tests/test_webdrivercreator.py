import unittest
from selenium_crawler.webdrivercreator import create_webdriver
from selenium.webdriver.remote.webdriver import WebDriver

class TestWebDriverCreator(unittest.TestCase):

    def test_create_webdriver_returns_webdriver(self):
        driver = None
        try:
            driver = create_webdriver()
            self.assertIsInstance(driver, WebDriver)
        finally:
            if driver:
                driver.quit()