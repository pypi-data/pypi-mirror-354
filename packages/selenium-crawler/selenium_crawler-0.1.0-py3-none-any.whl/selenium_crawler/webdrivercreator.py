import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


SHARED_MEM_PATH = "/dev/shm"


def create_webdriver(headless: bool = True, load_images: bool = False) -> WebDriver:
    """
    Creates an interoperable WebDriver. Method assumes 
    a Chrome installation existing on the system.
    ----------
    headless : bool
        If set to True browser will not open and run 
        headless. In case method is run in docker this 
        should be set to True (note, the default is 
        already True).
    """
    options = Options()

    # standard way of setting selenium to headless mode is
    # options.headless = True
    # however, this currently performs worse against bot detection
    # therefore we set it like this:
    if headless:
        options.add_argument("--headless=new")
    # avoid unneeded logs on windows systems
    options.add_argument("--log-level=3")
    # https://bugs.chromium.org/p/chromedriver/issues/detail?id=2907#c3
    # '--no-sandbox' is needed to run in linux without root
    options.add_argument("--no-sandbox")
    # avoid to load images
    if not load_images:
        options.add_argument('--blink-settings=imagesEnabled=false')
    # waits for document to be in a specific state
    # is default is 'normal' which equals
    # <code>document.readyState == 'complete'</code>
    # more details see W3C https://w3c.github.io/webdriver/#navigation
    options.page_load_strategy = 'eager'
    # Webdriver sometimes breaks due to the limited size of the shared memory in docker.
    # The following lines check the actual size of the shared memory in POSIX systems.
    # If it is to small we will use the "tmp" folder instead.
    # This will have a negative impact on performance.
    # Docker comes with a default size of 64 MB, this however can be changed.
    # (for more details refer to https://datawookie.dev/blog/2021/11/shared-memory-docker/)
    if os.path.exists(SHARED_MEM_PATH):
        file_system_size = os.statvfs(SHARED_MEM_PATH)  # type: ignore
        size_in_kb = file_system_size.f_frsize * file_system_size.f_blocks
        # check if size of shared memory is < 512
        if size_in_kb < 512 * (1024 * 1024):
            options.add_argument('--disable-dev-shm-usage')
    # After ChromeDriver 177 a DevToolsActivePorts created on 4533 which
    # creates issues in Docker. Therefore the port is deactivated.
    # (for more details refer to https://bugs.chromium.org/p/chromedriver/issues/detail?id=4403#c35)
    options.add_argument('--remote-debugging-pipe')
    # Disable the gpu as it is most likely not running attached to the docker container
    options.add_argument("--disable-gpu")
    # Add this line to help hide automation
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options, service=_create_service())

    _set_renderer(driver)
    _set_user_agent(driver)
    _set_navigator_webdriver(driver)

    return driver


def _set_navigator_webdriver(driver: WebDriver) -> None:
    # Ensure 'webdriver' is present in navigator, always returns false, and is non-writable/non-configurable
    script = """
    try {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
            set: () => {},
            configurable: false,
            enumerable: true
        });
    } catch (e) {}
    """
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": script}
    )


def _set_renderer(driver: WebDriver) -> None:
    # Inject script to spoof WebGL renderer and vendor
    script = '''
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        // 37445: UNMASKED_VENDOR_WEBGL, 37446: UNMASKED_RENDERER_WEBGL
        if (parameter === 37445) {
            return 'Intel Inc.';
        }
        if (parameter === 37446) {
            return 'Intel Iris OpenGL Engine';
        }
        return getParameter.call(this, parameter);
    };
    '''
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument", {"source": script})


def _set_user_agent(driver: WebDriver) -> None:
    # The Chrome Selenium driver comes with a default user agent such as:
    # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 HeadlessChrome/XX.XX.XX.XX
    # The method replaces "Headless" in the user agent string/header
    default_user_agent = driver.execute_script("return navigator.userAgent;")
    custom_user_agent = default_user_agent.replace("Headless", "")
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                           "userAgent": custom_user_agent})


def _create_service() -> Service:
    result = Service()

    # check if we are on windows
    if os.name == 'nt':
        # fix to ensure we do not get unnecessary log output like this:
        # "DevTools listening on ws://127.0.0.1:61165/devtools/browser/1cd3c683-bfac-4cb4-89e9-bf0cb3e3c4e9"
        # https://stackoverflow.com/a/71093078
        from subprocess import CREATE_NO_WINDOW
        result.creation_flags = CREATE_NO_WINDOW

    return result
