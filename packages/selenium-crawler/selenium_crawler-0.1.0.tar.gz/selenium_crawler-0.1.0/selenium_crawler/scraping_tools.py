from typing import Union
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

MAX_TIMEOUT_IN_SECONDS = 8.0


def get_clickable_element(element: Union[WebDriver, WebElement], mark: WebElement | tuple[str, str], timeout: float = MAX_TIMEOUT_IN_SECONDS) -> WebElement:
    """
    Waits until the element specified by 'mark' is clickable, then returns it.

    Args:
        element: The WebDriver or WebElement to search within.
        mark: A WebElement or a locator tuple (By, value).
        timeout: Maximum time to wait for the element to be clickable (in seconds).

    Returns:
        WebElement: The clickable element found.

    Raises:
        selenium.common.exceptions.TimeoutException: If the element is not clickable within the timeout.
    """
    element = WebDriverWait(element, timeout).until(
        EC.element_to_be_clickable(mark)
    )
    return element


def get_elements(element: Union[WebDriver, WebElement], locator: tuple[str, str], timeout: float = MAX_TIMEOUT_IN_SECONDS) -> list[WebElement]:
    """
    Waits until at least one element matching the locator is present, then returns all matching elements.

    Args:
        element: The WebDriver or WebElement to search within.
        locator: A tuple (By, value) to locate elements.
        timeout: Maximum time to wait for the elements to be present (in seconds).

    Returns:
        list[WebElement]: List of found elements (may be empty).

    Raises:
        selenium.common.exceptions.TimeoutException: If no element is found within the timeout.
    """
    WebDriverWait(element, timeout).until(
        EC.presence_of_element_located(locator)
    )
    elements = element.find_elements(locator[0], locator[1])
    return elements


def get_element(element: Union[WebDriver, WebElement], locator: tuple[str, str], timeout: float = MAX_TIMEOUT_IN_SECONDS) -> WebElement:
    """
    Waits until at least one element matching the locator is present, then returns the first matching element.

    Args:
        element: The WebDriver or WebElement to search within.
        locator: A tuple (By, value) to locate the element.
        timeout: Maximum time to wait for the element to be present (in seconds).

    Returns:
        WebElement: The first found element.

    Raises:
        selenium.common.exceptions.TimeoutException: If no element is found within the timeout.
        ValueError: If no element is found after waiting.
    """
    elements = get_elements(element, locator, timeout)
    if not elements:
        raise ValueError(f"could not find element for xpath: {locator}")
    return elements[0]
